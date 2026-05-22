# coding=utf-8
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.auth import Usuario
from routes.deps import get_current_user
from schemas.admin import DashboardMetrics, UsuarioResponse, ToggleUserStatus, ChangeUserRole
from schemas.unidad import UnidadBoardColumn
from services.admin_service import AdminService

router = APIRouter()

def require_admin(current_user: Usuario = Depends(get_current_user)):
    """Verifica explícitamente el rol de administrador"""
    es_admin = any(r.nombre == "administrador" for r in current_user.roles)
    if not es_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requiere rol de administrador."
        )
    return current_user

@router.get("/metrics", response_model=DashboardMetrics, dependencies=[Depends(require_admin)])
def obtener_metricas_dashboard(db: Session = Depends(get_db)):
    """Obtiene métricas globales para el panel administrativo"""
    return AdminService.get_dashboard_metrics(db)

@router.get("/remisiones-board", response_model=List[UnidadBoardColumn], dependencies=[Depends(require_admin)])
def obtener_remisiones_board(db: Session = Depends(get_db)):
    """Obtiene el Kanban board de remisiones activas por unidad"""
    return AdminService.get_active_remissions_board(db)

@router.get("/usuarios", response_model=List[UsuarioResponse], dependencies=[Depends(require_admin)])
def listar_usuarios(db: Session = Depends(get_db)):
    """Lista todos los usuarios del sistema (solo admin)"""
    return AdminService.list_users(db)

@router.patch("/usuarios/{user_id}/estado", dependencies=[Depends(require_admin)])
def cambiar_estado_usuario(
    user_id: int, 
    payload: ToggleUserStatus, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Activa o desactiva un usuario (solo admin)"""
    AdminService.toggle_user_status(db, current_user.id, user_id, payload.activo)
    return {"mensaje": f"Estado del usuario {user_id} actualizado a {'Activo' if payload.activo else 'Inactivo'}"}

@router.patch("/usuarios/{user_id}/rol", dependencies=[Depends(require_admin)])
def cambiar_rol_usuario(
    user_id: int, 
    payload: ChangeUserRole, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Cambia el rol de un usuario (solo admin)"""
    AdminService.change_user_role(db, current_user.id, user_id, payload.rol_id)
    return {"mensaje": f"Rol del usuario {user_id} actualizado con éxito."}

@router.get("/auditoria", dependencies=[Depends(require_admin)])
def obtener_auditoria(limit: int = 100, db: Session = Depends(get_db)):
    """Consulta los registros de auditoría (solo admin)"""
    return AdminService.get_audit_logs(db, limit)

