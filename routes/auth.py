# coding=utf-8
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.auth import UsuarioCreate, UsuarioLogin, UsuarioResponse
from controllers.auth_controller import AuthController
from routes.deps import get_current_user
from models.auth import Usuario

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

@router.post("/register")
def register(user_in: UsuarioCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario/enfermero"""
    return AuthController.register(db, user_in)

@router.post("/login")
def login(user_in: UsuarioLogin, db: Session = Depends(get_db)):
    """Iniciar sesión y obtener un token JWT"""
    return AuthController.login(db, user_in)

@router.post("/logout")
def logout(current_user: Usuario = Depends(get_current_user), db: Session = Depends(get_db)):
    """Cerrar sesión (revocar el JWT actual)"""
    return AuthController.logout(db, current_user.current_jti)

@router.get("/me", response_model=UsuarioResponse)
def read_users_me(current_user: Usuario = Depends(get_current_user)):
    """Obtener el perfil del usuario autenticado"""
    return current_user
