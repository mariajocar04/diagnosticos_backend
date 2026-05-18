# coding=utf-8
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UsuarioLogin(BaseModel):
    usuario: str
    password: str

class UsuarioCreate(BaseModel):
    usuario: str
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
