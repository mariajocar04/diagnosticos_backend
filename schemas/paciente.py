# coding=utf-8
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PacienteBase(BaseModel):
    nombre_completo: str = Field(..., max_length=120, description="Nombre completo del paciente")
    numero_historia: str = Field(..., max_length=20, description="Número único de historia clínica")
    tipo_documento: str = Field(..., max_length=20, description="Tipo de documento (e.g. cc, ti, pasaporte, rc, ce)")
    numero_documento: str = Field(..., max_length=20, description="Número de documento de identidad")

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(BaseModel):
    nombre_completo: Optional[str] = Field(None, max_length=120)
    numero_historia: Optional[str] = Field(None, max_length=20)
    tipo_documento: Optional[str] = Field(None, max_length=20)
    numero_documento: Optional[str] = Field(None, max_length=20)

class PacienteResponse(PacienteBase):
    id: int
    creado_en: datetime

    class Config:
        from_attributes = True

class PacienteList(BaseModel):
    total: int
    datos: List[PacienteResponse]

class UsuarioMiniResponse(BaseModel):
    id: int
    usuario: str
    nombre_completo: str

    class Config:
        from_attributes = True

class NotaEnfermeriaCreate(BaseModel):
    contenido: str = Field(..., description="Contenido de la nota de enfermería")

class NotaEnfermeriaResponse(BaseModel):
    id: int
    paciente_id: int
    usuario_id: int
    contenido: str
    creado_en: datetime
    usuario: Optional[UsuarioMiniResponse] = None

    class Config:
        from_attributes = True

class NotaEnfermeriaList(BaseModel):
    total: int
    datos: List[NotaEnfermeriaResponse]

class NandaMiniResponse(BaseModel):
    codigo: str
    nombre: str

    class Config:
        from_attributes = True

class DiagnosticoClinicoCreate(BaseModel):
    codigo_nanda: str = Field(..., max_length=10, description="Código del diagnóstico NANDA")
    resultado: Optional[str] = Field(None, description="Resultado esperado o evolución clínica")

class DiagnosticoClinicoResponse(BaseModel):
    id: int
    usuario_id: int
    paciente_id: int
    codigo_nanda: str
    resultado: Optional[str] = None
    fecha_hora: datetime
    usuario: Optional[UsuarioMiniResponse] = None
    catalogo: Optional[NandaMiniResponse] = None

    class Config:
        from_attributes = True

class EventoHistorialResponse(BaseModel):
    tipo: str  # 'nota' o 'diagnostico'
    id: int
    fecha: datetime
    descripcion: str
    detalle: str
    usuario: Optional[UsuarioMiniResponse] = None
    metadata: Optional[dict] = None
