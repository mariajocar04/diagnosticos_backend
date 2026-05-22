# coding=utf-8
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .remision import RemisionResponse

class UnidadBase(BaseModel):
    codigo: str
    nombre: str
    tipo: str
    capacidad: int
    descripcion: Optional[str] = None

class UnidadCreate(UnidadBase):
    pass

class UnidadUpdate(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    capacidad: Optional[int] = None
    descripcion: Optional[str] = None

class UnidadResponse(UnidadBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime
    pacientes_activos: Optional[int] = 0

    class Config:
        from_attributes = True

class UnidadList(BaseModel):
    total: int
    datos: List[UnidadResponse]

class UnidadBoardColumn(BaseModel):
    unidad: UnidadResponse
    remisiones_activas: List[RemisionResponse]
