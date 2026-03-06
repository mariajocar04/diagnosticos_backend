# coding=utf-8
from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from database import get_db
from models import Enfermero
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/enfermeros",
    tags=["Enfermeros"]
)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register")
async def register(
    usuario: str = Body(...),
    password: str = Body(...),
    nombre_completo: str = Body(None),
    db: Session = Depends(get_db)
):
    """Registrar un nuevo enfermero"""
    # Verificar si el usuario ya existe
    existing_user = db.query(Enfermero).filter(Enfermero.usuario == usuario).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    
    try:
        nuevo_enfermero = Enfermero(
            usuario=usuario,
            password_hash=get_password_hash(password),
            nombre_completo=nombre_completo
        )
        db.add(nuevo_enfermero)
        db.commit()
        db.refresh(nuevo_enfermero)
        return {"mensaje": "Enfermero registrado exitosamente", "id": nuevo_enfermero.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login(
    usuario: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    """Verificar credenciales de un enfermero"""
    enfermero = db.query(Enfermero).filter(Enfermero.usuario == usuario).first()
    if not enfermero or not verify_password(password, enfermero.password_hash):
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
    
    return {
        "mensaje": "Login exitoso",
        "datos": enfermero.to_dict()
    }

@router.get("/")
async def get_enfermeros(db: Session = Depends(get_db)):
    """Listar todos los enfermeros (sin contraseña)"""
    enfermeros = db.query(Enfermero).all()
    return [e.to_dict() for e in enfermeros]

@router.get("/{id}")
async def get_enfermero(id: int, db: Session = Depends(get_db)):
    """Obtener un enfermero por ID"""
    enfermero = db.query(Enfermero).filter(Enfermero.id == id).first()
    if not enfermero:
        raise HTTPException(status_code=404, detail="Enfermero no encontrado")
    return enfermero.to_dict()

@router.put("/update/{id}")
async def update_enfermero(
    id: int, 
    nombre_completo: str = Body(None),
    usuario: str = Body(None),
    password: str = Body(None),
    db: Session = Depends(get_db)
):
    """Actualizar datos de un enfermero"""
    enfermero = db.query(Enfermero).filter(Enfermero.id == id).first()
    if not enfermero:
        raise HTTPException(status_code=404, detail="Enfermero no encontrado")
    
    if usuario:
        # Verificar si el nuevo usuario ya existe en otro registro
        existing = db.query(Enfermero).filter(Enfermero.usuario == usuario, Enfermero.id != id).first()
        if existing:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
        enfermero.usuario = usuario
    
    if nombre_completo:
        enfermero.nombre_completo = nombre_completo
    
    if password:
        enfermero.password_hash = get_password_hash(password)
    
    try:
        db.commit()
        return {"mensaje": "Enfermero actualizado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{id}")
async def delete_enfermero(id: int, db: Session = Depends(get_db)):
    """Eliminar un enfermero"""
    enfermero = db.query(Enfermero).filter(Enfermero.id == id).first()
    if not enfermero:
        raise HTTPException(status_code=404, detail="Enfermero no encontrado")
    
    try:
        db.delete(enfermero)
        db.commit()
        return {"mensaje": "Enfermero eliminado correctamente", "id": id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
