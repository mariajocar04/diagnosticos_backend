# coding=utf-8
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class NandaCatalogoResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    sintomas: Optional[str] = None
    intervenciones_nic: Optional[str] = None
    resultados_noc: Optional[str] = None

    class Config:
        from_attributes = True

class NandaCatalogoList(BaseModel):
    total: int
    datos: List[NandaCatalogoResponse]

class ToggleFavoritoResponse(BaseModel):
    mensaje: str
    estado: bool

class BusquedaRecienteResponse(BaseModel):
    id: int
    termino: str
    fecha: datetime

    class Config:
        from_attributes = True

class BusquedaRecienteList(BaseModel):
    total: int
    datos: List[BusquedaRecienteResponse]

