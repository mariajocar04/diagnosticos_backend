# coding=utf-8
from typing import List, Optional
from sqlalchemy.orm import Session
from models.diagnostico import NandaCatalogo, Favorito
from models.auth import Usuario

class DiagnosticoService:

    @staticmethod
    def get_all_catalogo(db: Session, q: Optional[str] = None, user: Optional[Usuario] = None) -> List[NandaCatalogo]:
        # Verificar si el usuario es un profesional (Enfermero o Administrador registrado y activo)
        is_professional = False
        if user and user.activo:
            # Si el usuario tiene roles asignados, verificar si alguno es 'enfermero' o 'administrador'
            is_professional = any(role.nombre in ["enfermero", "administrador"] for role in user.roles)

        if is_professional:
            # Búsqueda flexible y sencilla (Enfermero/Admin)
            query = db.query(NandaCatalogo)
            if q:
                search_filter = f"%{q}%"
                query = query.filter(
                    (NandaCatalogo.codigo.ilike(search_filter)) |
                    (NandaCatalogo.nombre.ilike(search_filter)) |
                    (NandaCatalogo.sintomas.ilike(search_filter))
                )
            return query.order_by(NandaCatalogo.codigo).all()
        else:
            # Búsqueda restrictiva (Invitado / Público)
            if not q or not q.strip():
                return []  # El invitado no ve el catálogo completo por defecto sin buscar
            
            # Tokenizar por comas, limpiar espacios y omitir términos vacíos
            terms = [t.strip().lower() for t in q.split(",") if t.strip()]
            
            # Si ingresó menos de 2 términos, es imposible cumplir con la regla de 2 o más coincidencias
            if len(terms) < 2:
                return []
                
            # Recuperar el catálogo para evaluar las coincidencias en memoria
            all_diagnoses = db.query(NandaCatalogo).all()
            filtered_results = []
            
            for diag in all_diagnoses:
                # Obtener la lista de síntomas del diagnóstico desde el string CSV
                diag_sintomas = [s.strip().lower() for s in (diag.sintomas or "").split(",") if s.strip()]
                
                # Contar cuántos términos buscados coinciden/están contenidos en los síntomas de este diagnóstico
                matches = 0
                for term in terms:
                    if any(term in s for s in diag_sintomas):
                        matches += 1
                        
                if matches >= 2:
                    filtered_results.append(diag)
                    
            # Ordenar por código para consistencia
            filtered_results.sort(key=lambda x: x.codigo)
            return filtered_results

    @staticmethod
    def get_catalogo_by_id_or_codigo(db: Session, id_or_codigo: str) -> Optional[NandaCatalogo]:
        # Intentar buscar por ID si es un número, de lo contrario buscar por código
        if id_or_codigo.isdigit():
            row = db.query(NandaCatalogo).filter(NandaCatalogo.id == int(id_or_codigo)).first()
            if row:
                return row
        return db.query(NandaCatalogo).filter(NandaCatalogo.codigo == id_or_codigo).first()

    @staticmethod
    def get_favoritos_by_user(db: Session, user_id: int) -> List[NandaCatalogo]:
        # Hacemos un join explícito para obtener los catálogos NANDA que son favoritos del usuario
        return db.query(NandaCatalogo).join(
            Favorito, Favorito.codigo_nanda == NandaCatalogo.codigo
        ).filter(
            Favorito.usuario_id == user_id
        ).order_by(Favorito.creado_en.desc()).all()

    @staticmethod
    def toggle_favorito(db: Session, user_id: int, codigo_nanda: str) -> bool:
        # Verificar si el diagnóstico existe
        diagnostico = db.query(NandaCatalogo).filter(NandaCatalogo.codigo == codigo_nanda).first()
        if not diagnostico:
            raise ValueError(f"El diagnóstico con código {codigo_nanda} no existe.")

        favorito = db.query(Favorito).filter(
            Favorito.usuario_id == user_id, 
            Favorito.codigo_nanda == codigo_nanda
        ).first()

        if favorito:
            # Ya es favorito, desmarcarlo
            db.delete(favorito)
            db.commit()
            return False
        else:
            # No es favorito, agregarlo
            nuevo_favorito = Favorito(usuario_id=user_id, codigo_nanda=codigo_nanda)
            db.add(nuevo_favorito)
            db.commit()
            return True
