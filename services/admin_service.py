# coding=utf-8
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List
from fastapi import HTTPException, status

from models import Usuario, Rol, UsuarioRol, Paciente, DiagnosticoClinico, ReporteExportado, Auditoria, Unidad, Remision
from schemas.admin import DashboardMetrics

class AdminService:
    @staticmethod
    def get_dashboard_metrics(db: Session) -> DashboardMetrics:
        usuarios_activos = db.query(Usuario).filter(Usuario.activo == True).count()
        pacientes_totales = db.query(Paciente).count()
        
        # Diagnósticos de los últimos 7 días
        hace_7_dias = datetime.now() - timedelta(days=7)
        diagnosticos_recientes = db.query(DiagnosticoClinico).filter(DiagnosticoClinico.fecha_hora >= hace_7_dias).count()
        
        pdfs_generados = db.query(ReporteExportado).count()
        remisiones_activas = db.query(Remision).filter(Remision.estado == 'ACTIVA').count()
        
        # Pacientes por unidad (Donut chart data)
        unidades = db.query(Unidad).all()
        pacientes_por_unidad = []
        for u in unidades:
            count = db.query(Remision).filter(Remision.unidad_id == u.id, Remision.estado == 'ACTIVA').count()
            if count > 0:
                pacientes_por_unidad.append({"unidad": u.nombre, "cantidad": count})
        
        return DashboardMetrics(
            usuarios_activos=usuarios_activos,
            pacientes_totales=pacientes_totales,
            diagnosticos_recientes=diagnosticos_recientes,
            pdfs_generados=pdfs_generados,
            remisiones_activas=remisiones_activas,
            pacientes_por_unidad=pacientes_por_unidad
        )

    @staticmethod
    def get_active_remissions_board(db: Session):
        unidades = db.query(Unidad).all()
        board = []
        for u in unidades:
            # Traer remisiones que estén en estado PENDIENTE o ACTIVA
            remisiones = db.query(Remision).filter(
                Remision.unidad_id == u.id, 
                Remision.estado.in_(['PENDIENTE', 'ACTIVA'])
            ).order_by(Remision.fecha_remision.desc()).all()
            
            # Calcular ocupación real (solo los pacientes con estado ACTIVA ocupan cama)
            pacientes_activos = sum(1 for r in remisiones if r.estado == 'ACTIVA')
            
            # Formatear unidad y remisiones para coincidir con UnidadBoardColumn
            unidad_dict = {
                "codigo": u.codigo,
                "nombre": u.nombre,
                "tipo": u.tipo,
                "capacidad": u.capacidad,
                "descripcion": u.descripcion,
                "id": u.id,
                "creado_en": u.creado_en,
                "actualizado_en": u.actualizado_en,
                "pacientes_activos": pacientes_activos
            }
            board.append({
                "unidad": unidad_dict,
                "remisiones_activas": remisiones
            })
        return board

    @staticmethod
    def list_users(db: Session) -> List[dict]:
        usuarios = db.query(Usuario).all()
        result = []
        for u in usuarios:
            result.append({
                "id": u.id,
                "usuario": u.usuario,
                "email": u.email,
                "nombre_completo": u.nombre_completo,
                "activo": u.activo,
                "creado_en": u.creado_en,
                "roles": [r.nombre for r in u.roles]
            })
        return result

    @staticmethod
    def toggle_user_status(db: Session, admin_id: int, user_id: int, active: bool) -> bool:
        if admin_id == user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes cambiar tu propio estado.")
            
        usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
            
        usuario.activo = active
        
        # Auditoría
        auditoria = Auditoria(
            usuario_id=admin_id,
            recurso="usuario",
            accion="actualizar_estado",
            detalles=f"Usuario {user_id} {'activado' if active else 'desactivado'}"
        )
        db.add(auditoria)
        db.commit()
        return True

    @staticmethod
    def change_user_role(db: Session, admin_id: int, user_id: int, rol_id: int) -> bool:
        if admin_id == user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No puedes cambiar tu propio rol.")
            
        usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
            
        rol = db.query(Rol).filter(Rol.id == rol_id).first()
        if not rol:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rol no encontrado")
            
        # Limpiar roles anteriores (en MVP solo hay un rol por usuario)
        db.query(UsuarioRol).filter(UsuarioRol.usuario_id == user_id).delete()
        
        # Asignar nuevo rol
        nuevo_rol = UsuarioRol(usuario_id=user_id, rol_id=rol_id)
        db.add(nuevo_rol)
        
        # Auditoría
        auditoria = Auditoria(
            usuario_id=admin_id,
            recurso="usuario",
            accion="actualizar_rol",
            detalles=f"Rol del usuario {user_id} cambiado a {rol.nombre}"
        )
        db.add(auditoria)
        db.commit()
        return True

    @staticmethod
    def get_audit_logs(db: Session, limit: int = 100):
        return db.query(Auditoria).order_by(Auditoria.fecha_hora.desc()).limit(limit).all()
