# coding=utf-8
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.auth import UsuarioCreate, UsuarioLogin, UsuarioResponse, OTPRequest, OTPVerify, PasswordResetByOTP
from controllers.auth_controller import AuthController
from routes.deps import get_current_user
from models.auth import Usuario
from services.auth_service import AuthService
from services.email_service import EmailService

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


@router.post('/otp/request')
async def request_otp(payload: OTPRequest, db: Session = Depends(get_db)):
    """Solicitar codigo OTP alfanumerico para recuperacion de contrasena."""
    otp_code = AuthService.create_password_reset_otp(db, payload.email)
    if otp_code:
        await EmailService.send_otp_email(payload.email, otp_code)

    # Respuesta neutral para no exponer si el correo existe
    return {'mensaje': 'Si el correo existe, se envio un codigo OTP de recuperacion'}


@router.post('/otp/verify')
def verify_otp(payload: OTPVerify, db: Session = Depends(get_db)):
    """Verificar OTP y devolver token temporal para reset de contrasena."""
    reset_token = AuthService.verify_password_reset_otp(db, payload.email, payload.otp_code)
    if not reset_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='OTP invalido, expirado o agotado')

    return {'reset_token': reset_token, 'token_type': 'bearer'}


@router.post('/password/reset')
def reset_password(payload: PasswordResetByOTP, db: Session = Depends(get_db)):
    """Cambiar contrasena usando reset_token emitido tras verificar OTP."""
    ok = AuthService.reset_password_with_token(db, payload.reset_token, payload.new_password)
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token invalido o expirado')

    return {'mensaje': 'Contrasena actualizada correctamente'}
