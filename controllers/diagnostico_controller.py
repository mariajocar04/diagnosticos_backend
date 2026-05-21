# coding=utf-8
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from services.diagnostico_service import DiagnosticoService

class DiagnosticoController:

    @staticmethod
    def get_catalogo(db: Session, q: str = None, user = None):
        rows = DiagnosticoService.get_all_catalogo(db, q=q, user=user)
        return {"total": len(rows), "datos": rows}

    @staticmethod
    def get_catalogo_by_id_or_codigo(db: Session, id_or_codigo: str):
        row = DiagnosticoService.get_catalogo_by_id_or_codigo(db, id_or_codigo)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diagnóstico NANDA no encontrado en el catálogo"
            )
        return row

    @staticmethod
    def get_favoritos(db: Session, user_id: int):
        rows = DiagnosticoService.get_favoritos_by_user(db, user_id)
        return {"total": len(rows), "datos": rows}

    @staticmethod
    def toggle_favorito(db: Session, user_id: int, codigo_nanda: str):
        try:
            estado = DiagnosticoService.toggle_favorito(db, user_id, codigo_nanda)
            mensaje = "Diagnóstico agregado a favoritos" if estado else "Diagnóstico eliminado de favoritos"
            return {"mensaje": mensaje, "estado": estado}
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
