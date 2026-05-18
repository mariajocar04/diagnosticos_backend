# coding=utf-8
import os
import sys

# Agregar la raíz al path para importar módulos correctamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import engine
from models.base import Base
# Importar todos los modelos
from models import *

def update_db():
    print("Verificando y creando tablas faltantes en MySQL...")
    print("Base de datos destino:", engine.url)
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas actualizadas exitosamente sin borrar datos.")

if __name__ == "__main__":
    update_db()
