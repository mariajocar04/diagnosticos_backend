# coding=utf-8
import os
import sys

# Agregar la raíz al path para importar módulos correctamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import engine
from models.base import Base
# Importar todos los modelos a través de __init__ para que Base.metadata los registre
from models import *
# Importar funciones de siembra
from seed_diagnosticos import seed_diagnosticos
from seed_enfermeros import seed_enfermeros
from seed_remisiones import seed

def reset_db():
    print("⚠️ ATENCIÓN: Se eliminarán todas las tablas de MySQL y sus datos.")
    print("Base de datos destino:", engine.url)
    respuesta = input("¿Estás seguro de continuar? (s/N): ")
    if respuesta.lower() != 's':
        print("Operación cancelada.")
        return

    print("Eliminando tablas...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creando tablas limpias...")
    Base.metadata.create_all(bind=engine)
    print("✅ Base de datos reseteada y tablas creadas exitosamente.\n")
    
    print("Iniciando poblamiento de datos (Semillas)...")
    try:
        seed_diagnosticos()
        seed_enfermeros()
        seed()
        print("\n✅ Base de datos completamente poblada y lista.")
    except Exception as e:
        print(f"\n❌ Error al ejecutar las semillas: {e}")

if __name__ == "__main__":
    reset_db()
