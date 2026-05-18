# coding=utf-8
from typing import List, Optional
from sqlalchemy.orm import Session
from models.diagnostico import NandaCatalogo

class DiagnosticoService:

    @staticmethod
    def get_all_catalogo(db: Session, q: Optional[str] = None) -> List[NandaCatalogo]:
        query = db.query(NandaCatalogo)
        if q:
            # Búsqueda insensible a mayúsculas/minúsculas en código, nombre y síntomas
            search_filter = f"%{q}%"
            query = query.filter(
                (NandaCatalogo.codigo.ilike(search_filter)) |
                (NandaCatalogo.nombre.ilike(search_filter)) |
                (NandaCatalogo.sintomas.ilike(search_filter))
            )
        return query.order_by(NandaCatalogo.codigo).all()

    @staticmethod
    def get_catalogo_by_id_or_codigo(db: Session, id_or_codigo: str) -> Optional[NandaCatalogo]:
        # Intentar buscar por ID si es un número, de lo contrario buscar por código
        if id_or_codigo.isdigit():
            row = db.query(NandaCatalogo).filter(NandaCatalogo.id == int(id_or_codigo)).first()
            if row:
                return row
        return db.query(NandaCatalogo).filter(NandaCatalogo.codigo == id_or_codigo).first()
