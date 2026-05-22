# coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Remision(Base):
    __tablename__ = 'remision'
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey('paciente.id', ondelete='CASCADE'), nullable=False)
    unidad_id = Column(Integer, ForeignKey('unidad.id', ondelete='RESTRICT'), nullable=False)
    motivo = Column(Text)
    prioridad = Column(String(10), nullable=False, server_default='MEDIA')
    estado = Column(String(20), nullable=False, server_default='PENDIENTE')
    asignado_por = Column(Integer, ForeignKey('usuario.id', ondelete='SET NULL'), nullable=True)
    fecha_remision = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_ingreso = Column(DateTime(timezone=True), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    paciente = relationship('Paciente')
    unidad = relationship('Unidad')
    asignador = relationship('Usuario', foreign_keys=[asignado_por])

    def __repr__(self):
        return f"<Remision {self.id} paciente={self.paciente_id} unidad={self.unidad_id}>"


class OtpToken(Base):
    __tablename__ = 'otp_token'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id', ondelete='CASCADE'), nullable=False)
    token_hash = Column(String(200), nullable=False)
    tipo = Column(String(50), nullable=False)
    usado = Column(Boolean, nullable=False, server_default='0')
    intentos = Column(Integer, nullable=False, server_default='0')
    expiracion = Column(DateTime(timezone=True), nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    usuario = relationship('Usuario')

    def __repr__(self):
        return f"<OtpToken user={self.usuario_id} tipo={self.tipo} usado={self.usado}>"
