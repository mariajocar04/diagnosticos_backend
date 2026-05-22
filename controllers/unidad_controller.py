# coding=utf-8
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from services.unidad_service import UnidadService
from schemas.unidad import UnidadCreate, UnidadUpdate

class UnidadController:
    @staticmethod
    def crear_unidad(db: Session, data: UnidadCreate):
        try:
            return UnidadService.crear_unidad(db, data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @staticmethod
    def obtener_unidad(db: Session, unidad_id: int):
        unidad = UnidadService.obtener_unidad_por_id(db, unidad_id)
        if not unidad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Unidad no encontrada')
        return unidad

    @staticmethod
    def listar_unidades(db: Session, skip: int = 0, limit: int = 100):
        datos, total = UnidadService.listar_unidades(db, skip=skip, limit=limit)
        return {"total": total, "datos": datos}

    @staticmethod
    def actualizar_unidad(db: Session, unidad_id: int, data: UnidadUpdate):
        try:
            return UnidadService.actualizar_unidad(db, unidad_id, data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
