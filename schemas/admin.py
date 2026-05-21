# coding=utf-8
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DashboardMetrics(BaseModel):
    usuarios_activos: int
    pacientes_totales: int
    diagnosticos_recientes: int
    pdfs_generados: int

class UsuarioResponse(BaseModel):
    id: int
    usuario: str
    email: str
    nombre_completo: Optional[str]
    activo: bool
    creado_en: datetime
    roles: List[str]

    class Config:
        from_attributes = True

class ToggleUserStatus(BaseModel):
    activo: bool

class ChangeUserRole(BaseModel):
    rol_id: int
