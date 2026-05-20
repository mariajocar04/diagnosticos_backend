# coding=utf-8
import os
import jwt
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models.auth import Usuario
from services.auth_service import AuthService, SECRET_KEY, ALGORITHM

security = HTTPBearer()
security_optional = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_str: str = payload.get("sub")
        jti: str = payload.get("jti")
        
        if email_str is None or jti is None:
            raise credentials_exception
            
        # Verificar si la sesión fue revocada (Logout)
        if AuthService.is_token_revoked(db, jti=jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="La sesión ha expirado o ha sido cerrada",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = db.query(Usuario).filter(Usuario.email == email_str).first()
    if user is None:
        raise credentials_exception
    if not user.activo:
        raise HTTPException(status_code=400, detail="El usuario está inactivo")
        
    # Añadimos el token jti al objeto user temporalmente si es necesario para logout
    user.current_jti = jti
    return user

def check_permission(permiso_requerido: str):
    """
    Dependencia para RBAC. Verifica que el usuario tenga el permiso requerido en sus roles.
    """
    def _check(current_user: Usuario = Depends(get_current_user)):
        # El administrador tiene acceso total por defecto
        if any(role.nombre == "administrador" for role in current_user.roles):
            return current_user
            
        # Extraer todos los códigos de permisos asociados a los roles del usuario
        permisos_usuario = {
            permiso.codigo 
            for role in current_user.roles 
            for permiso in role.permisos
        }
        
        if permiso_requerido not in permisos_usuario:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere el permiso: {permiso_requerido}"
            )
            
        return current_user
    return _check

def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional),
    db: Session = Depends(get_db)
) -> Optional[Usuario]:
    """
    Extrae el usuario actual si se proporciona un token válido, de lo contrario retorna None sin lanzar excepción.
    """
    if not credentials:
        return None
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_str: str = payload.get("sub")
        jti: str = payload.get("jti")
        
        if email_str is None or jti is None:
            return None
            
        # Verificar si la sesión fue revocada (Logout)
        if AuthService.is_token_revoked(db, jti=jti):
            return None
            
    except jwt.PyJWTError:
        return None
        
    user = db.query(Usuario).filter(Usuario.email == email_str).first()
    if user is None or not user.activo:
        return None
        
    user.current_jti = jti
    return user

