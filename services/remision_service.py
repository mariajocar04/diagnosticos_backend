# coding=utf-8
from sqlalchemy.orm import Session
from typing import Optional, Tuple, List
from fastapi import HTTPException, status
from models import Remision, Unidad, Paciente, Usuario

class RemisionService:
    @staticmethod
    def crear_remision(db: Session, data) -> Remision:
        # Verificar paciente
        paciente = db.query(Paciente).filter(Paciente.id == data.paciente_id).first()
        if not paciente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Paciente no encontrado')

        unidad = db.query(Unidad).filter(Unidad.id == data.unidad_id).first()
        if not unidad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Unidad no encontrada')

        nueva = Remision(
            paciente_id=data.paciente_id,
            unidad_id=data.unidad_id,
            motivo=data.motivo,
            prioridad=data.prioridad or 'MEDIA'
        )
        db.add(nueva)
        db.commit()
        db.refresh(nueva)
        return nueva

    @staticmethod
    def obtener_remision_por_id(db: Session, remision_id: int) -> Optional[Remision]:
        return db.query(Remision).filter(Remision.id == remision_id).first()

    @staticmethod
    def listar_remisiones(db: Session, skip: int = 0, limit: int = 100, unidad_id: Optional[int] = None, estado: Optional[str] = None) -> Tuple[List[Remision], int]:
        query = db.query(Remision)
        if unidad_id:
            query = query.filter(Remision.unidad_id == unidad_id)
        if estado:
            query = query.filter(Remision.estado == estado)
        total = query.count()
        datos = query.order_by(Remision.creado_en.desc()).offset(skip).limit(limit).all()
        return datos, total

    @staticmethod
    def actualizar_remision(db: Session, remision_id: int, data) -> Remision:
        rem = db.query(Remision).filter(Remision.id == remision_id).first()
        if not rem:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Remisión no encontrada')
        if data.unidad_id:
            unidad = db.query(Unidad).filter(Unidad.id == data.unidad_id).first()
            if not unidad:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Unidad no encontrada')
            rem.unidad_id = data.unidad_id
        if data.motivo is not None:
            rem.motivo = data.motivo
        if data.prioridad is not None:
            rem.prioridad = data.prioridad
        if data.estado is not None:
            rem.estado = data.estado
        db.commit()
        db.refresh(rem)
        return rem

    @staticmethod
    def cambiar_estado(db: Session, remision_id: int, nuevo_estado: str) -> Remision:
        rem = db.query(Remision).filter(Remision.id == remision_id).first()
        if not rem:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Remisión no encontrada')
        rem.estado = nuevo_estado
        if nuevo_estado == 'ACTIVA':
            from sqlalchemy import func
            rem.fecha_ingreso = func.now()
        db.commit()
        db.refresh(rem)
        return rem
