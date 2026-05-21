# coding=utf-8
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.auth import Usuario
from routes.deps import get_current_user, check_permission
from services.reporte_service import ReporteService
from schemas.reporte import ReporteExportadoResponse

router = APIRouter()

@router.get("/paciente/{paciente_id}/pdf", dependencies=[Depends(check_permission("reporte:exportar_propio"))])
def exportar_pdf_paciente(
    paciente_id: int, 
    db: Session = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    """
    Genera y devuelve un reporte clínico PDF del paciente.
    """
    pdf_buffer, nombre_archivo = ReporteService.generar_pdf_paciente(db, paciente_id, current_user.id)
    
    headers = {
        'Content-Disposition': f'attachment; filename="{nombre_archivo}"'
    }
    
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)

@router.get("/historial", response_model=List[ReporteExportadoResponse])
def historial_exportaciones(
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Devuelve el historial de PDFs generados.
    """
    return ReporteService.obtener_historial_exportaciones(db, limit)
