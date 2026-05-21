# coding=utf-8
from pydantic import BaseModel
from typing import List
from datetime import datetime

class ReporteExportadoBase(BaseModel):
    paciente_id: int
    nombre_archivo: str

class ReporteExportadoResponse(ReporteExportadoBase):
    id: int
    usuario_id: int
    generado_en: datetime

    class Config:
        from_attributes = True
