# coding=utf-8
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from models import Usuario
from services.paciente_service import PacienteService
from schemas.paciente import (
    PacienteCreate, PacienteUpdate, PacienteResponse, PacienteList,
    NotaEnfermeriaCreate, NotaEnfermeriaResponse, NotaEnfermeriaList,
    DiagnosticoClinicoCreate, DiagnosticoClinicoResponse, EventoHistorialResponse
)

class PacienteController:
    @staticmethod
    def crear_paciente(db: Session, data: PacienteCreate) -> PacienteResponse:
        return PacienteService.crear_paciente(db, data)

    @staticmethod
    def obtener_paciente_por_id(db: Session, paciente_id: int) -> PacienteResponse:
        paciente = PacienteService.obtener_paciente_por_id(db, paciente_id)
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        return paciente

    @staticmethod
    def obtener_pacientes(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None
    ) -> PacienteList:
        datos, total = PacienteService.obtener_pacientes(db, skip, limit, search)
        return PacienteList(total=total, datos=datos)

    @staticmethod
    def actualizar_paciente(db: Session, paciente_id: int, data: PacienteUpdate) -> PacienteResponse:
        return PacienteService.actualizar_paciente(db, paciente_id, data)

    @staticmethod
    def eliminar_paciente(db: Session, paciente_id: int):
        PacienteService.eliminar_paciente(db, paciente_id)
        return {"mensaje": "Paciente eliminado exitosamente"}

    @staticmethod
    def crear_nota(db: Session, paciente_id: int, usuario_id: int, data: NotaEnfermeriaCreate) -> NotaEnfermeriaResponse:
        return PacienteService.crear_nota(db, paciente_id, usuario_id, data)

    @staticmethod
    def obtener_notas_paciente(db: Session, paciente_id: int, usuario_id: Optional[int] = None) -> NotaEnfermeriaList:
        datos = PacienteService.obtener_notas_paciente(db, paciente_id, usuario_id)
        return NotaEnfermeriaList(total=len(datos), datos=datos)

    @staticmethod
    def eliminar_nota(db: Session, nota_id: int, current_user: Usuario):
        PacienteService.eliminar_nota(db, nota_id, current_user)
        return {"mensaje": "Nota de enfermería eliminada exitosamente"}

    @staticmethod
    def asignar_diagnostico(db: Session, usuario_id: int, paciente_id: int, data: DiagnosticoClinicoCreate) -> DiagnosticoClinicoResponse:
        return PacienteService.asignar_diagnostico(db, usuario_id, paciente_id, data)

    @staticmethod
    def obtener_diagnosticos_paciente(db: Session, paciente_id: int) -> list[DiagnosticoClinicoResponse]:
        return PacienteService.obtener_diagnosticos_paciente(db, paciente_id)

    @staticmethod
    def desasignar_diagnostico(db: Session, asignacion_id: int):
        PacienteService.desasignar_diagnostico(db, asignacion_id)
        return {"mensaje": "Diagnóstico clínico desasignado exitosamente"}

    @staticmethod
    def obtener_historial_paciente(db: Session, paciente_id: int, usuario_id_filtro: Optional[int] = None) -> list[EventoHistorialResponse]:
        return PacienteService.obtener_historial_paciente(db, paciente_id, usuario_id_filtro)
