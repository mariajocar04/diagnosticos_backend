# coding=utf-8
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class UsuarioCreate(BaseModel):
    usuario: str
    email: EmailStr
    password: str
    nombre_completo: str

class RolResponse(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class UsuarioResponse(BaseModel):
    id: int
    usuario: str
    email: EmailStr
    nombre_completo: Optional[str] = None
    activo: bool
    roles: List[RolResponse] = []

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    usuario: Optional[str] = None
    jti: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str


class OTPRequest(BaseModel):
    email: EmailStr


class OTPVerify(BaseModel):
    email: EmailStr
    otp_code: str


class PasswordResetByOTP(BaseModel):
    reset_token: str
    new_password: str
