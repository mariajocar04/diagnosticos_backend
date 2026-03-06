# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Enfermero, Base
from database import DATABASE_URL
from passlib.context import CryptContext

# Configuración de hashing (debe coincidir con la de las rutas)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def seed_enfermeros():
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    print("Insertando registros de prueba en la tabla 'enfermeros'...")

    enfermeros_data = [
        {"usuario": "angela_k", "password": "password123", "nombre_completo": "Angela Kemer"},
        {"usuario": "juan_perez", "password": "admin456", "nombre_completo": "Juan Pérez"},
        {"usuario": "maria_garcia", "password": "nurse789", "nombre_completo": "Maria García"},
        {"usuario": "admin", "password": "rootpassword", "nombre_completo": "Administrador General"},
        {"usuario": "carlos_m", "password": "securePass01", "nombre_completo": "Carlos Mendoza"}
    ]

    for data in enfermeros_data:
        # Verificar si ya existe para evitar duplicados
        existing = db.query(Enfermero).filter(Enfermero.usuario == data["usuario"]).first()
        if not existing:
            nuevo = Enfermero(
                usuario=data["usuario"],
                password_hash=get_password_hash(data["password"]),
                nombre_completo=data["nombre_completo"]
            )
            db.add(nuevo)
            print(f"Agregado: {data['usuario']}")
        else:
            print(f"Saltado (ya existe): {data['usuario']}")

    try:
        db.commit()
        print("\n¡Registros de prueba insertados exitosamente!")
    except Exception as e:
        db.rollback()
        print(f"Error al insertar registros: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_enfermeros()
