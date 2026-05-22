# coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class NandaCatalogo(Base):
    __tablename__ = "nanda_catalogo"
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(10), unique=True, index=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    sintomas = Column(Text)
    intervenciones_nic = Column(Text)
    resultados_noc = Column(Text)

class DiagnosticoClinico(Base):
    __tablename__ = "diagnostico_clinico"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    paciente_id = Column(Integer, ForeignKey("paciente.id", ondelete="CASCADE"), nullable=False)
    codigo_nanda = Column(String(10), ForeignKey("nanda_catalogo.codigo", ondelete="CASCADE"), nullable=False)
    resultado = Column(Text)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
    remision_id = Column(Integer, ForeignKey('remision.id', ondelete='SET NULL'), nullable=True)
    
    paciente = relationship("Paciente")
    catalogo = relationship("NandaCatalogo")
    usuario = relationship("Usuario")
    remision = relationship('Remision', foreign_keys=[remision_id])

class NotaEnfermeria(Base):
    __tablename__ = "nota_enfermeria"
    id = Column(Integer, primary_key=True, autoincrement=True)
    paciente_id = Column(Integer, ForeignKey("paciente.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    contenido = Column(Text, nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    remision_id = Column(Integer, ForeignKey('remision.id', ondelete='SET NULL'), nullable=True)
    
    paciente = relationship("Paciente")
    usuario = relationship("Usuario")
    remision = relationship('Remision', foreign_keys=[remision_id])

class Favorito(Base):
    __tablename__ = "favorito"
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), primary_key=True)
    codigo_nanda = Column(String(10), ForeignKey("nanda_catalogo.codigo", ondelete="CASCADE"), primary_key=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

class BusquedaReciente(Base):
    __tablename__ = "busqueda_reciente"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    termino = Column(String(200), nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())

class ReporteExportado(Base):
    __tablename__ = "reporte_exportado"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="CASCADE"), nullable=False)
    paciente_id = Column(Integer, ForeignKey("paciente.id", ondelete="CASCADE"), nullable=False)
    nombre_archivo = Column(Text, nullable=False)
    generado_en = Column(DateTime(timezone=True), server_default=func.now())
