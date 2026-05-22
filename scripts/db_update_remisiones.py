# coding=utf-8
"""
Script de actualización de base de datos no destructivo para agregar tablas
`unidad`, `remision`, `otp_token` y columnas `remision_id` en tablas existentes.

Uso:
    python scripts/db_update_remisiones.py

Este script usa el `engine` definido en `database.py` y aplica cambios mínimos:
- Crea las tablas nuevas si no existen (SQLAlchemy create_all sobre las tablas nuevas).
- Añade columnas `remision_id` mediante ALTER TABLE sólo si no existen.

NOTA: Ejecutar en staging antes de producción. Hacer backup previo.
"""

from sqlalchemy import inspect, text
from database import engine, SessionLocal
from sqlalchemy.exc import SQLAlchemyError

# Importar modelos para que sus MetaData sean visibles
from models.unidad import Unidad
from models.remision import Remision, OtpToken

inspector = inspect(engine)

def create_tables():
    # create_all sobre las tablas nuevas solo
    Unidade_table = Unidad.__table__
    Remision_table = Remision.__table__
    Otp_table = OtpToken.__table__
    print('Creando tablas nuevas si no existen...')
    Unidade_table.create(bind=engine, checkfirst=True)
    Remision_table.create(bind=engine, checkfirst=True)
    Otp_table.create(bind=engine, checkfirst=True)
    print('Tablas creadas/verificadas.')

def add_column_if_missing(table_name, column_def_sql, fk_sql=None):
    cols = [c['name'] for c in inspector.get_columns(table_name)]
    if column_def_sql is None:
        return
    col_name = column_def_sql.split()[0]
    if col_name in cols:
        print(f'Columna {col_name} ya existe en {table_name}, omitiendo.')
        return
    with engine.connect() as conn:
        try:
            print(f'Agregando columna {col_name} a {table_name}...')
            conn.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_def_sql}"))
            if fk_sql:
                print(f'Agregando FK para {col_name}...')
                conn.execute(text(fk_sql))
            print(f'Columna {col_name} agregada en {table_name}.')
        except SQLAlchemyError as e:
            print('Error al agregar columna:', e)

def main():
    create_tables()

    # Añadir remision_id a diagnostico_clinico
    if 'diagnostico_clinico' in inspector.get_table_names():
        add_column_if_missing(
            'diagnostico_clinico',
            "remision_id INT NULL",
            "ALTER TABLE diagnostico_clinico ADD CONSTRAINT fk_diagnostico_remision FOREIGN KEY (remision_id) REFERENCES remision(id) ON DELETE SET NULL"
        )
    else:
        print('Tabla diagnostico_clinico no encontrada; omitiendo agregar columna remision_id.')

    # Añadir remision_id a nota_enfermeria
    if 'nota_enfermeria' in inspector.get_table_names():
        add_column_if_missing(
            'nota_enfermeria',
            "remision_id INT NULL",
            "ALTER TABLE nota_enfermeria ADD CONSTRAINT fk_nota_remision FOREIGN KEY (remision_id) REFERENCES remision(id) ON DELETE SET NULL"
        )
    else:
        print('Tabla nota_enfermeria no encontrada; omitiendo agregar columna remision_id.')

    print('Actualización completa. Revisa los registros y relaciones.')

if __name__ == '__main__':
    main()
