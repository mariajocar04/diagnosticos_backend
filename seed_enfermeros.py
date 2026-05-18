# coding=utf-8
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Asegurar que se encuentra en la ruta del backend
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database import DATABASE_URL
from models import Usuario, Rol, UsuarioRol
from services.auth_service import AuthService

def seed_enfermeros():
    load_dotenv()
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    print("Insertando roles por defecto...")
    roles_data = [
        {"nombre": "administrador", "descripcion": "Administrador del sistema con acceso completo"},
        {"nombre": "enfermero", "descripcion": "Personal de enfermería con acceso a pacientes y diagnósticos"}
    ]
    
    roles_map = {}
    for r_data in roles_data:
        existing_rol = db.query(Rol).filter(Rol.nombre == r_data["nombre"]).first()
        if not existing_rol:
            rol = Rol(nombre=r_data["nombre"], descripcion=r_data["descripcion"])
            db.add(rol)
            db.flush() # Para obtener el ID generado sin comprometer la transacción todavía
            roles_map[r_data["nombre"]] = rol
            print(f"Rol creado: {r_data['nombre']}")
        else:
            roles_map[r_data["nombre"]] = existing_rol
            print(f"Rol ya existe: {r_data['nombre']}")

    print("\nInsertando usuarios de prueba en la tabla 'usuario'...")

    enfermeros_data = [
        {"usuario": "angela_k", "email": "angela_k@ticos.com", "password": "password123", "nombre_completo": "Angela Kemer", "rol": "enfermero"},
        {"usuario": "juan_perez", "email": "juan_perez@ticos.com", "password": "admin456", "nombre_completo": "Juan Pérez", "rol": "enfermero"},
        {"usuario": "maria_garcia", "email": "maria_garcia@ticos.com", "password": "nurse789", "nombre_completo": "Maria García", "rol": "enfermero"},
        {"usuario": "admin", "email": "admin@ticos.com", "password": "rootpassword", "nombre_completo": "Administrador General", "rol": "administrador"},
        {"usuario": "carlos_m", "email": "carlos_m@ticos.com", "password": "securePass01", "nombre_completo": "Carlos Mendoza", "rol": "enfermero"}
    ]

    for data in enfermeros_data:
        # Verificar si el usuario o correo ya existe
        existing = db.query(Usuario).filter(
            (Usuario.usuario == data["usuario"]) | (Usuario.email == data["email"])
        ).first()
        
        if not existing:
            nuevo = Usuario(
                usuario=data["usuario"],
                email=data["email"],
                password_hash=AuthService.get_password_hash(data["password"]),
                nombre_completo=data["nombre_completo"]
            )
            db.add(nuevo)
            db.flush() # Obtener ID del usuario
            
            # Asociar rol
            rol_objetivo = roles_map[data["rol"]]
            user_rol = UsuarioRol(usuario_id=nuevo.id, rol_id=rol_objetivo.id)
            db.add(user_rol)
            
            print(f"Agregado usuario: {data['usuario']} con rol {data['rol']}")
        else:
            print(f"Saltado (ya existe usuario o email): {data['usuario']}")

    try:
        db.commit()
        print("\n¡Registros de usuarios y roles insertados exitosamente!")
    except Exception as e:
        db.rollback()
        print(f"Error al insertar registros: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_enfermeros()
