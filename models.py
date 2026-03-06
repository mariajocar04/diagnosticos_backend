# coding=utf-8
from sqlalchemy import Column, Integer, String, Text, inspect
from database import Base

class Diagnostico(Base):
    __tablename__ = "diagnosticos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    codigo = Column(String(10))
    nombre = Column(String(255))
    sintomas = Column(Text)
    intervenciones_nic = Column(Text)
    resultados_noc = Column(Text)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

class Enfermero(Base):
    __tablename__ = "enfermeros"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombre_completo = Column(String(255))

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != 'password_hash'}
