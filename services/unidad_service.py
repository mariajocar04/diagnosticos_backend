# coding=utf-8
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from models.unidad import Unidad
from models.remision import Remision
from schemas.unidad import UnidadCreate, UnidadUpdate

class UnidadService:
    @staticmethod
    def crear_unidad(db: Session, data: UnidadCreate):
        existente = db.query(Unidad).filter(Unidad.codigo == data.codigo).first()
        if existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El código de unidad ya existe.")
        
        unidad = Unidad(**data.dict())
        db.add(unidad)
        db.commit()
        db.refresh(unidad)
        return unidad

    @staticmethod
    def listar_unidades(db: Session, skip: int = 0, limit: int = 100):
        unidades = db.query(Unidad).offset(skip).limit(limit).all()
        
        # Calcular pacientes activos por unidad
        unidades_con_activos = []
        for u in unidades:
            activos = db.query(Remision).filter(Remision.unidad_id == u.id, Remision.estado == 'ACTIVA').count()
            u.pacientes_activos = activos
            unidades_con_activos.append(u)
            
        total = db.query(Unidad).count()
        return unidades_con_activos, total

    @staticmethod
    def obtener_unidad_por_id(db: Session, unidad_id: int):
        unidad = db.query(Unidad).filter(Unidad.id == unidad_id).first()
        if unidad:
            unidad.pacientes_activos = db.query(Remision).filter(Remision.unidad_id == unidad_id, Remision.estado == 'ACTIVA').count()
        return unidad

    @staticmethod
    def actualizar_unidad(db: Session, unidad_id: int, data: UnidadUpdate):
        unidad = db.query(Unidad).filter(Unidad.id == unidad_id).first()
        if not unidad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unidad no encontrada")

        update_data = data.dict(exclude_unset=True)
        if "codigo" in update_data and update_data["codigo"] != unidad.codigo:
            existente = db.query(Unidad).filter(Unidad.codigo == update_data["codigo"]).first()
            if existente:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El código de unidad ya existe.")

        for key, value in update_data.items():
            setattr(unidad, key, value)

        db.commit()
        db.refresh(unidad)
        unidad.pacientes_activos = db.query(Remision).filter(Remision.unidad_id == unidad_id, Remision.estado == 'ACTIVA').count()
        return unidad
