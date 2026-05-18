# coding=utf-8
import os
import uuid
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
import jwt
from sqlalchemy.orm import Session
from models.auth import Usuario, Sesion

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
    def authenticate_user(db: Session, usuario: str, password: str) -> Optional[Usuario]:
        user = db.query(Usuario).filter(Usuario.usuario == usuario).first()
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
