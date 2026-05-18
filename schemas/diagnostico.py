# coding=utf-8
from pydantic import BaseModel
from typing import Optional, List

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
