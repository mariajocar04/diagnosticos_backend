# coding=utf-8
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from schemas.remision import RemisionCreate, RemisionResponse, RemisionList, RemisionUpdate
from controllers.remision_controller import RemisionController
from routes.deps import get_current_user, check_permission

router = APIRouter(
    prefix="/remisiones",
    tags=["Remisiones"]
)


@router.post("", response_model=RemisionResponse)
def crear_remision(data: RemisionCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Crear una remisión para un paciente (requiere autenticación)."""
    return RemisionController.crear_remision(db, data)


@router.get("", response_model=RemisionList)
def listar_remisiones(skip: int = 0, limit: int = 100, unidad_id: Optional[int] = None, estado: Optional[str] = None, db: Session = Depends(get_db), current_user=Depends(check_permission("remision:gestionar"))):
    """Listar remisiones (permiso requerido para ver)."""
    return RemisionController.listar_remisiones(db, skip=skip, limit=limit, unidad_id=unidad_id, estado=estado)


@router.get("/{remision_id}", response_model=RemisionResponse)
def obtener_remision(remision_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Obtener detalle de una remisión por ID (requiere autenticación)."""
    return RemisionController.obtener_remision(db, remision_id)


@router.put("/{remision_id}", response_model=RemisionResponse)
def actualizar_remision(remision_id: int, data: RemisionUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Actualizar una remisión (requiere autenticación)."""
    return RemisionController.actualizar_remision(db, remision_id, data)


@router.post("/{remision_id}/estado")
def cambiar_estado(remision_id: int, estado: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Cambiar el estado de una remisión (requiere autenticación)."""
    return RemisionController.cambiar_estado(db, remision_id, estado)
