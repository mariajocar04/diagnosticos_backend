# coding=utf-8
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.unidad import UnidadCreate, UnidadResponse, UnidadList, UnidadUpdate
from controllers.unidad_controller import UnidadController
from routes.deps import get_current_user, check_permission

router = APIRouter(
    prefix="/unidades",
    tags=["Unidades"]
)

@router.post("", response_model=UnidadResponse)
def crear_unidad(data: UnidadCreate, db: Session = Depends(get_db), current_user=Depends(check_permission("admin"))):
    """Crear una unidad (requiere permiso admin)."""
    return UnidadController.crear_unidad(db, data)

@router.get("", response_model=UnidadList)
def listar_unidades(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Listar unidades (requiere autenticación)."""
    return UnidadController.listar_unidades(db, skip=skip, limit=limit)

@router.get("/{unidad_id}", response_model=UnidadResponse)
def obtener_unidad(unidad_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Obtener detalle de una unidad por ID (requiere autenticación)."""
    return UnidadController.obtener_unidad(db, unidad_id)

@router.put("/{unidad_id}", response_model=UnidadResponse)
def actualizar_unidad(unidad_id: int, data: UnidadUpdate, db: Session = Depends(get_db), current_user=Depends(check_permission("admin"))):
    """Actualizar una unidad (requiere permiso admin)."""
    return UnidadController.actualizar_unidad(db, unidad_id, data)
