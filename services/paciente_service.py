# coding=utf-8
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List, Tuple
from fastapi import HTTPException, status
from models import Paciente, NotaEnfermeria, Usuario
from schemas.paciente import PacienteCreate, PacienteUpdate, NotaEnfermeriaCreate

class PacienteService:
    @staticmethod
    def crear_paciente(db: Session, data: PacienteCreate) -> Paciente:
        # Verificar unicidad de numero_historia
        historia_existente = db.query(Paciente).filter(Paciente.numero_historia == data.numero_historia).first()
        if historia_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un paciente con el número de historia clínica: {data.numero_historia}"
            )
        
        # Verificar unicidad de tipo_documento + numero_documento
        documento_existente = db.query(Paciente).filter(
            Paciente.tipo_documento == data.tipo_documento,
            Paciente.numero_documento == data.numero_documento
        ).first()
        if documento_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un paciente con el documento: {data.tipo_documento.upper()} {data.numero_documento}"
            )
            
        nuevo_paciente = Paciente(
            nombre_completo=data.nombre_completo,
            numero_historia=data.numero_historia,
            tipo_documento=data.tipo_documento,
            numero_documento=data.numero_documento
        )
        db.add(nuevo_paciente)
        db.commit()
        db.refresh(nuevo_paciente)
        return nuevo_paciente

    @staticmethod
    def obtener_paciente_por_id(db: Session, paciente_id: int) -> Optional[Paciente]:
        return db.query(Paciente).filter(Paciente.id == paciente_id).first()

    @staticmethod
    def obtener_paciente_por_historia(db: Session, numero_historia: str) -> Optional[Paciente]:
        return db.query(Paciente).filter(Paciente.numero_historia == numero_historia).first()

    @staticmethod
    def obtener_pacientes(
        db: Session, 
        skip: int = 0, 
        limit: int = 100, 
        search: Optional[str] = None
    ) -> Tuple[List[Paciente], int]:
        query = db.query(Paciente)
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Paciente.nombre_completo.ilike(search_filter),
                    Paciente.numero_documento.ilike(search_filter),
                    Paciente.numero_historia.ilike(search_filter)
                )
            )
        total = query.count()
        datos = query.order_by(Paciente.creado_en.desc()).offset(skip).limit(limit).all()
        return datos, total

    @staticmethod
    def actualizar_paciente(db: Session, paciente_id: int, data: PacienteUpdate) -> Optional[Paciente]:
        paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
            
        # Validar numero_historia si cambia
        if data.numero_historia and data.numero_historia != paciente.numero_historia:
            existente = db.query(Paciente).filter(
                Paciente.numero_historia == data.numero_historia,
                Paciente.id != paciente_id
            ).first()
            if existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro paciente con la historia clínica: {data.numero_historia}"
                )
            paciente.numero_historia = data.numero_historia

        # Validar tipo/numero documento si alguno cambia
        nuevo_tipo = data.tipo_documento or paciente.tipo_documento
        nuevo_num = data.numero_documento or paciente.numero_documento
        if (data.tipo_documento or data.numero_documento) and (nuevo_tipo != paciente.tipo_documento or nuevo_num != paciente.numero_documento):
            existente = db.query(Paciente).filter(
                Paciente.tipo_documento == nuevo_tipo,
                Paciente.numero_documento == nuevo_num,
                Paciente.id != paciente_id
            ).first()
            if existente:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro paciente con el documento: {nuevo_tipo.upper()} {nuevo_num}"
                )
            paciente.tipo_documento = nuevo_tipo
            paciente.numero_documento = nuevo_num

        if data.nombre_completo:
            paciente.nombre_completo = data.nombre_completo

        db.commit()
        db.refresh(paciente)
        return paciente

    @staticmethod
    def eliminar_paciente(db: Session, paciente_id: int) -> bool:
        paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        db.delete(paciente)
        db.commit()
        return True

    @staticmethod
    def crear_nota(db: Session, paciente_id: int, usuario_id: int, data: NotaEnfermeriaCreate) -> NotaEnfermeria:
        # Verificar que el paciente exista
        paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        
        nueva_nota = NotaEnfermeria(
            paciente_id=paciente_id,
            usuario_id=usuario_id,
            contenido=data.contenido
        )
        db.add(nueva_nota)
        db.commit()
        db.refresh(nueva_nota)
        return nueva_nota

    @staticmethod
    def obtener_notas_paciente(db: Session, paciente_id: int, usuario_id: Optional[int] = None) -> List[NotaEnfermeria]:
        # Verificar que el paciente exista
        paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado"
            )
        
        query = db.query(NotaEnfermeria).filter(NotaEnfermeria.paciente_id == paciente_id)
        if usuario_id is not None:
            query = query.filter(NotaEnfermeria.usuario_id == usuario_id)
            
        return query.order_by(NotaEnfermeria.creado_en.desc()).all()

    @staticmethod
    def eliminar_nota(db: Session, nota_id: int, current_user: Usuario) -> bool:
        nota = db.query(NotaEnfermeria).filter(NotaEnfermeria.id == nota_id).first()
        if not nota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota de enfermería no encontrada"
            )
            
        # Verificar si es administrador o si es el autor
        is_admin = any(role.nombre == "administrador" for role in current_user.roles)
        if not is_admin and nota.usuario_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado. Solo el creador de la nota o un administrador pueden eliminarla."
            )
            
        db.delete(nota)
        db.commit()
        return True
