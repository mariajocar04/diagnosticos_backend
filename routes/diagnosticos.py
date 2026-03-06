# coding=utf-8
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Diagnostico

router = APIRouter(
    prefix="/diagnosticos",
    tags=["Diagnosticos NANDA"]
)

@router.get("/")
async def get_all(db: Session = Depends(get_db)):
    """Obtener todos los diagnósticos"""
    rows = db.query(Diagnostico).order_by(Diagnostico.id).all()
    return {"total": len(rows), "datos": [r.to_dict() for r in rows]}

@router.get("/{id}")
async def get_one(id: int, db: Session = Depends(get_db)):
    """Obtener un diagnóstico por ID"""
    row = db.query(Diagnostico).filter(Diagnostico.id == id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    return row.to_dict()

@router.post("/insert")
async def insert(
    codigo: str, 
    nombre: str, 
    sintomas: str, 
    intervenciones_nic: str, 
    resultados_noc: str, 
    db: Session = Depends(get_db)
):
    """Insertar un nuevo diagnóstico"""
    try:
        nuevo = Diagnostico(
            codigo=codigo,
            nombre=nombre,
            sintomas=sintomas,
            intervenciones_nic=intervenciones_nic,
            resultados_noc=resultados_noc
        )
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return {"mensaje": "Creado exitosamente", "id": nuevo.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update/{id}")
async def update(id: int, campo: str, valor: str, db: Session = Depends(get_db)):
    """Actualizar un campo dinámicamente"""
    row = db.query(Diagnostico).filter(Diagnostico.id == id).first()
    if not row:
        raise HTTPException(status_code=404, detail="No encontrado")
    
    if hasattr(row, campo):
        setattr(row, campo, valor)
        db.commit()
        return {"mensaje": "Actualizado", "campo": campo, "nuevo_valor": valor}
    else:
        raise HTTPException(status_code=400, detail=f"Campo '{campo}' no existe")

@router.delete("/delete/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    """Eliminar un diagnóstico"""
    row = db.query(Diagnostico).filter(Diagnostico.id == id).first()
    if not row:
        raise HTTPException(status_code=404, detail="No encontrado")
    
    try:
        db.delete(row)
        db.commit()
        return {"mensaje": "Eliminado ✅", "id_eliminado": id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
