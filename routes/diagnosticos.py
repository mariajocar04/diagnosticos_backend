# coding=utf-8
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from schemas.diagnostico import NandaCatalogoList, NandaCatalogoResponse
from controllers.diagnostico_controller import DiagnosticoController
from routes.deps import get_current_user_optional
from models.auth import Usuario

router = APIRouter(
    prefix="/diagnosticos",
    tags=["Catálogo NANDA (Público)"]
)

@router.get("", response_model=NandaCatalogoList)
def get_catalogo(
    q: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Optional[Usuario] = Depends(get_current_user_optional)
):
    """
    [Modo Invitado / Público] Obtener listado de diagnósticos NANDA.
    Permite filtrar por código, nombre o síntomas usando el parámetro 'q'.
    Aplica búsqueda dual: restrictiva para invitados, sencilla para profesionales.
    """
    return DiagnosticoController.get_catalogo(db, q=q, user=current_user)

@router.get("/{id_or_codigo}", response_model=NandaCatalogoResponse)
def get_catalogo_by_id_or_codigo(id_or_codigo: str, db: Session = Depends(get_db)):
    """
    [Modo Invitado / Público] Obtener detalles completos de un diagnóstico NANDA por su ID o Código.
    """
    return DiagnosticoController.get_catalogo_by_id_or_codigo(db, id_or_codigo)
