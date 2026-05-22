# coding=utf-8
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from services.remision_service import RemisionService
from schemas.remision import RemisionCreate, RemisionUpdate

class RemisionController:
    @staticmethod
    def crear_remision(db: Session, data: RemisionCreate):
        try:
            return RemisionService.crear_remision(db, data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @staticmethod
    def obtener_remision(db: Session, remision_id: int):
        rem = RemisionService.obtener_remision_por_id(db, remision_id)
        if not rem:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Remisión no encontrada')
        return rem

    @staticmethod
    def listar_remisiones(db: Session, skip: int = 0, limit: int = 100, unidad_id: int = None, estado: str = None):
        datos, total = RemisionService.listar_remisiones(db, skip=skip, limit=limit, unidad_id=unidad_id, estado=estado)
        return {"total": total, "datos": datos}

    @staticmethod
    def actualizar_remision(db: Session, remision_id: int, data: RemisionUpdate):
        try:
            return RemisionService.actualizar_remision(db, remision_id, data)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    @staticmethod
    def cambiar_estado(db: Session, remision_id: int, nuevo_estado: str):
        try:
            return RemisionService.cambiar_estado(db, remision_id, nuevo_estado)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
