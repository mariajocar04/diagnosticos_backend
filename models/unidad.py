# coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .base import Base

class Unidad(Base):
    __tablename__ = 'unidad'
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), nullable=False, unique=True)
    nombre = Column(String(200), nullable=False)
    tipo = Column(String(50), nullable=False)
    capacidad = Column(Integer, nullable=False, default=0)
    descripcion = Column(Text)
    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    actualizado_en = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Unidad {self.codigo} - {self.nombre}>"
