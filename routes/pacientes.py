# coding=utf-8
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from routes.deps import check_permission, get_current_user
from models.auth import Usuario
from schemas.paciente import (
    PacienteCreate, PacienteUpdate, PacienteResponse, PacienteList,
    NotaEnfermeriaCreate, NotaEnfermeriaResponse, NotaEnfermeriaList,
    DiagnosticoClinicoCreate, DiagnosticoClinicoResponse, EventoHistorialResponse
)
from controllers.paciente_controller import PacienteController

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)

@router.post("", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
def crear_paciente(
    data: PacienteCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(check_permission("paciente:crear"))
):
    return PacienteController.crear_paciente(db, data)

@router.get("", response_model=PacienteList)
def obtener_pacientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None, description="Búsqueda por nombre, documento o historia clínica"),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(check_permission("paciente:leer"))
):
    return PacienteController.obtener_pacientes(db, skip, limit, search)

@router.get("/{paciente_id}", response_model=PacienteResponse)
def obtener_paciente_por_id(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(check_permission("paciente:leer"))
):
    return PacienteController.obtener_paciente_por_id(db, paciente_id)

@router.put("/{paciente_id}", response_model=PacienteResponse)
def actualizar_paciente(
    paciente_id: int,
    data: PacienteUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(check_permission("paciente:editar"))
):
    return PacienteController.actualizar_paciente(db, paciente_id, data)

@router.delete("/{paciente_id}", status_code=status.HTTP_200_OK)
def eliminar_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Solo el rol 'administrador' puede eliminar pacientes
    is_admin = any(role.nombre == "administrador" for role in current_user.roles)
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Solo los administradores pueden eliminar pacientes."
        )
    return PacienteController.eliminar_paciente(db, paciente_id)

@router.post("/{paciente_id}/notas", response_model=NotaEnfermeriaResponse, status_code=status.HTTP_201_CREATED)
def crear_nota(
    paciente_id: int,
    data: NotaEnfermeriaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(check_permission("nota:crear"))
):
    return PacienteController.crear_nota(db, paciente_id, current_user.id, data)

@router.get("/{paciente_id}/notas", response_model=NotaEnfermeriaList)
def obtener_notas_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(check_permission("nota:leer_propio"))
):
    # Si no es admin, solo puede leer las suyas
    is_admin = any(role.nombre == "administrador" for role in current_user.roles)
    usuario_id_filtro = current_user.id if not is_admin else None
    return PacienteController.obtener_notas_paciente(db, paciente_id, usuario_id_filtro)

@router.delete("/notas/{nota_id}", status_code=status.HTTP_200_OK)
def eliminar_nota(
    nota_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return PacienteController.eliminar_nota(db, nota_id, current_user)

@router.post("/{paciente_id}/diagnosticos", response_model=DiagnosticoClinicoResponse, status_code=status.HTTP_201_CREATED)
def asignar_diagnostico(
    paciente_id: int,
    data: DiagnosticoClinicoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(check_permission("paciente:editar"))
):
    return PacienteController.asignar_diagnostico(db, current_user.id, paciente_id, data)

@router.get("/{paciente_id}/diagnosticos", response_model=list[DiagnosticoClinicoResponse])
def obtener_diagnosticos_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(check_permission("paciente:leer"))
):
    return PacienteController.obtener_diagnosticos_paciente(db, paciente_id)

@router.delete("/diagnosticos/{asignacion_id}", status_code=status.HTTP_200_OK)
def desasignar_diagnostico(
    asignacion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(check_permission("paciente:editar"))
):
    return PacienteController.desasignar_diagnostico(db, asignacion_id)

@router.get("/{paciente_id}/historial", response_model=list[EventoHistorialResponse])
def obtener_historial_paciente(
    paciente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(check_permission("paciente:leer"))
):
    # Si no es admin, aplicamos restricción nota:leer_propio en el historial unificado
    is_admin = any(role.nombre == "administrador" for role in current_user.roles)
    usuario_id_filtro = current_user.id if not is_admin else None
    return PacienteController.obtener_historial_paciente(db, paciente_id, usuario_id_filtro)
