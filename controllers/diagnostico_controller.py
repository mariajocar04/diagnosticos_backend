# coding=utf-8
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from services.diagnostico_service import DiagnosticoService

class DiagnosticoController:

    @staticmethod
    def get_catalogo(db: Session, q: str = None):
        rows = DiagnosticoService.get_all_catalogo(db, q=q)
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
