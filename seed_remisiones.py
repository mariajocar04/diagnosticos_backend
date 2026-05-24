# coding=utf-8
"""
Seed inicial para `unidad` y una remisión de ejemplo.

Uso:
    python seed_remisiones.py

Este script usa `SessionLocal` desde `database.py`.
"""
from database import SessionLocal
from models.unidad import Unidad
from models.remision import Remision
from sqlalchemy.exc import SQLAlchemyError

def seed():
    db = SessionLocal()
    try:
        unidades = [
            {'codigo': 'UCI-AD', 'nombre': 'UCI Adultos', 'tipo': 'UCI', 'descripcion': 'Unidad de cuidados intensivos para adultos', 'capacidad': 10},
            {'codigo': 'URG-AD', 'nombre': 'Urgencias Adultos', 'tipo': 'URGENCIAS', 'descripcion': 'Unidad de urgencias', 'capacidad': 15},
            {'codigo': 'PISO-3', 'nombre': 'Piso 3 Medicina', 'tipo': 'PISO', 'descripcion': 'Piso 3 - Medicina', 'capacidad': 20},
        ]
        for u in unidades:
            exists = db.query(Unidad).filter(Unidad.codigo == u['codigo']).first()
            if not exists:
                db.add(Unidad(**u))
        db.commit()
        print('Seeds de unidades aplicadas.')

        # Inserción de remisión de ejemplo sólo si existe paciente con id=1
        paciente = db.execute('SELECT id FROM paciente WHERE id=1').fetchone()
        unidad = db.query(Unidad).filter(Unidad.codigo == 'UCI-AD').first()
        if paciente and unidad:
            exists_r = db.query(Remision).filter(Remision.paciente_id == 1).first()
            if not exists_r:
                r = Remision(paciente_id=1, unidad_id=unidad.id, motivo='Insuficiencia respiratoria', prioridad='ALTA', estado='PENDIENTE', asignado_por=None)
                db.add(r)
                db.commit()
                print('Remisión de ejemplo creada para paciente id=1.')
        else:
            print('Paciente id=1 no encontrado o unidad UCI-AD falta; no se crea remisión de ejemplo.')

    except SQLAlchemyError as e:
        db.rollback()
        print('Error al aplicar seeds:', e)
    finally:
        db.close()

if __name__ == '__main__':
    seed()
