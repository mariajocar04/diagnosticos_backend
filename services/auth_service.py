# coding=utf-8
import os
import uuid
import string
import secrets
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
import jwt
from sqlalchemy.orm import Session
from models.auth import Usuario, Sesion
from models.remision import OtpToken

# Configuración de JWT
SECRET_KEY = os.getenv("SECRET_KEY", "secret_dev_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class AuthService:
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[Usuario]:
        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user:
            return None
        if not AuthService.verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, db: Session, user_id: int) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Generar un JTI único para esta sesión
        jti = str(uuid.uuid4())
        to_encode.update({"exp": expire, "jti": jti})
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        # Registrar la sesión en la base de datos
        db_sesion = Sesion(usuario_id=user_id, jti=jti)
        db.add(db_sesion)
        db.commit()
        
        return encoded_jwt

    @staticmethod
    def revoke_token(db: Session, jti: str) -> bool:
        sesion = db.query(Sesion).filter(Sesion.jti == jti).first()
        if sesion and not sesion.revocado:
            sesion.revocado = True
            db.commit()
            return True
        return False
        
    @staticmethod
    def is_token_revoked(db: Session, jti: str) -> bool:
        sesion = db.query(Sesion).filter(Sesion.jti == jti).first()
        if not sesion or sesion.revocado:
            return True
        return False

    @staticmethod
    def generate_otp_code(length: int = 8) -> str:
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    @staticmethod
    def create_password_reset_otp(db: Session, email: str, minutes_valid: int = 15) -> Optional[str]:
        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user:
            return None

        # Invalidar tokens anteriores no usados
        previous = db.query(OtpToken).filter(
            OtpToken.usuario_id == user.id,
            OtpToken.tipo == 'password_reset',
            OtpToken.usado == False
        ).all()
        for p in previous:
            p.usado = True

        otp_code = AuthService.generate_otp_code()
        token_hash = AuthService.get_password_hash(otp_code)
        expires_at = datetime.utcnow() + timedelta(minutes=minutes_valid)

        row = OtpToken(
            usuario_id=user.id,
            token_hash=token_hash,
            tipo='password_reset',
            expiracion=expires_at,
            usado=False,
            intentos=0,
        )
        db.add(row)
        db.commit()
        return otp_code

    @staticmethod
    def verify_password_reset_otp(db: Session, email: str, otp_code: str, max_attempts: int = 5) -> Optional[str]:
        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user:
            return None

        now = datetime.utcnow()
        otp_row = db.query(OtpToken).filter(
            OtpToken.usuario_id == user.id,
            OtpToken.tipo == 'password_reset',
            OtpToken.usado == False,
            OtpToken.expiracion > now
        ).order_by(OtpToken.creado_en.desc()).first()

        if not otp_row:
            return None

        if not AuthService.verify_password(otp_code, otp_row.token_hash):
            otp_row.intentos = (otp_row.intentos or 0) + 1
            if otp_row.intentos >= max_attempts:
                otp_row.usado = True
            db.commit()
            return None

        otp_row.usado = True
        db.commit()

        payload = {
            'sub': user.email,
            'purpose': 'password_reset',
            'exp': datetime.utcnow() + timedelta(minutes=15)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def reset_password_with_token(db: Session, reset_token: str, new_password: str) -> bool:
        try:
            payload = jwt.decode(reset_token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get('sub')
            purpose = payload.get('purpose')
            if not email or purpose != 'password_reset':
                return False
        except jwt.PyJWTError:
            return False

        user = db.query(Usuario).filter(Usuario.email == email).first()
        if not user:
            return False

        user.password_hash = AuthService.get_password_hash(new_password)
        db.commit()
        return True
