# coding=utf-8
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UnidadResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    tipo: str
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

class RemisionCreate(BaseModel):
    paciente_id: int = Field(...)
    unidad_id: int = Field(...)
    motivo: Optional[str] = None
    prioridad: Optional[str] = Field('MEDIA')

class RemisionUpdate(BaseModel):
    unidad_id: Optional[int] = None
    motivo: Optional[str] = None
    prioridad: Optional[str] = None
    estado: Optional[str] = None

class RemisionResponse(BaseModel):
    id: int
    paciente_id: int
    unidad: Optional[UnidadResponse] = None
    motivo: Optional[str] = None
    prioridad: str
    estado: str
    asignado_por: Optional[int] = None
    fecha_remision: datetime
    fecha_ingreso: Optional[datetime] = None
    creado_en: datetime

    class Config:
        from_attributes = True

class RemisionList(BaseModel):
    total: int
    datos: List[RemisionResponse]
