# coding=utf-8
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .base import Base

class Paciente(Base):
    __tablename__ = "paciente"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_completo = Column(String(120), nullable=False)
    numero_historia = Column(String(20), unique=True, nullable=False, index=True)
    tipo_documento = Column(String(20), nullable=False)
    numero_documento = Column(String(20), nullable=False, index=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
