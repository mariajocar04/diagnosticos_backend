# coding=utf-8
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.auth import Usuario
from schemas.auth import UsuarioCreate, UsuarioLogin
from services.auth_service import AuthService

class AuthController:
    
    @staticmethod
    def register(db: Session, user_in: UsuarioCreate):
        # Verificar si el usuario o el email ya existen
        existing_user = db.query(Usuario).filter(
            (Usuario.usuario == user_in.usuario) | (Usuario.email == user_in.email)
        ).first()
        if existing_user:
            if existing_user.usuario == user_in.usuario:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de usuario ya está registrado"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El correo electrónico ya está registrado"
                )
        
        nuevo_usuario = Usuario(
            usuario=user_in.usuario,
            email=user_in.email,
            password_hash=AuthService.get_password_hash(user_in.password),
            nombre_completo=user_in.nombre_completo
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return {"mensaje": "Usuario registrado exitosamente", "id": nuevo_usuario.id}

    @staticmethod
    def login(db: Session, user_in: UsuarioLogin):
        user = AuthService.authenticate_user(db, user_in.usuario, user_in.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario está inactivo"
            )
            
        access_token = AuthService.create_access_token(data={"sub": user.usuario}, db=db, user_id=user.id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "usuario": user
        }

    @staticmethod
    def logout(db: Session, jti: str):
        revocado = AuthService.revoke_token(db, jti)
        if not revocado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La sesión ya estaba cerrada o el token es inválido"
            )
        return {"mensaje": "Cierre de sesión exitoso"}
