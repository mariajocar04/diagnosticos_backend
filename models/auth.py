# coding=utf-8
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Rol(Base):
    __tablename__ = "rol"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255))
    
    permisos = relationship("Permiso", secondary="rol_permiso", back_populates="roles")
    usuarios = relationship("Usuario", secondary="usuario_rol", back_populates="roles")

class Permiso(Base):
    __tablename__ = "permiso"
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(100), unique=True, nullable=False) # e.g. 'paciente:crear'
    recurso = Column(String(50), nullable=False)
    accion = Column(String(50), nullable=False)
    
    roles = relationship("Rol", secondary="rol_permiso", back_populates="permisos")

class RolPermiso(Base):
    __tablename__ = "rol_permiso"
    rol_id = Column(Integer, ForeignKey("rol.id", ondelete="CASCADE"), primary_key=True)
    permiso_id = Column(Integer, ForeignKey("permiso.id", ondelete="CASCADE"), primary_key=True)

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombre_completo = Column(String(255))
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    
    roles = relationship("Rol", secondary="usuario_rol", back_populates="usuarios")
    sesiones = relationship("Sesion", back_populates="usuario")

class UsuarioRol(Base):
    __tablename__ = "usuario_rol"
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), primary_key=True)
    rol_id = Column(Integer, ForeignKey("rol.id", ondelete="CASCADE"), primary_key=True)

class Sesion(Base):
    __tablename__ = "sesion"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    jti = Column(String(255), unique=True, nullable=False, index=True)
    revocado = Column(Boolean, default=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    
    usuario = relationship("Usuario", back_populates="sesiones")

class Auditoria(Base):
    __tablename__ = "auditoria"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="SET NULL"), nullable=True)
    recurso = Column(String(50), nullable=False)
    accion = Column(String(50), nullable=False)
    detalles = Column(String(500))
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
