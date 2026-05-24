# coding=utf-8
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.auth import Usuario, Rol, UsuarioRol
from schemas.auth import UsuarioCreate, UsuarioLogin, UsuarioUpdate
from services.auth_service import AuthService

class AuthController:
    
    @staticmethod
    def register(db: Session, user_in: UsuarioCreate):
        # Verificar si el usuario o el email ya existen
        existing_user = db.query(Usuario).filter(
            (Usuario.usuario == user_in.usuario) | (Usuario.email == user_in.email)
        ).first()
        if existing_user:
            if existing_user.usuario == user_in.usuario:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de usuario ya está registrado"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El correo electrónico ya está registrado"
                )
        
        nuevo_usuario = Usuario(
            usuario=user_in.usuario,
            email=user_in.email,
            password_hash=AuthService.get_password_hash(user_in.password),
            nombre_completo=user_in.nombre_completo
        )
        db.add(nuevo_usuario)
        db.flush() # Obtener ID del usuario para asociar el rol

        # Asignación automática y temporal del rol 'enfermero'
        rol_enfermero = db.query(Rol).filter(Rol.nombre == "enfermero").first()
        if rol_enfermero:
            usuario_rol = UsuarioRol(usuario_id=nuevo_usuario.id, rol_id=rol_enfermero.id)
            db.add(usuario_rol)

        db.commit()
        db.refresh(nuevo_usuario)
        return {"mensaje": "Usuario registrado exitosamente", "id": nuevo_usuario.id}

    @staticmethod
    def login(db: Session, user_in: UsuarioLogin):
        user = AuthService.authenticate_user(db, user_in.email, user_in.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario está inactivo"
            )
            
        access_token = AuthService.create_access_token(data={"sub": user.email}, db=db, user_id=user.id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "usuario": user
        }

    @staticmethod
    def logout(db: Session, jti: str):
        revocado = AuthService.revoke_token(db, jti)
        if not revocado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La sesión ya estaba cerrada o el token es inválido"
            )
        return {"mensaje": "Cierre de sesión exitoso"}

    @staticmethod
    def update_me(db: Session, current_user: Usuario, data: UsuarioUpdate):
        if data.usuario is not None and data.usuario.strip() != "":
            # Verificar si ya existe el nombre de usuario
            existing = db.query(Usuario).filter(Usuario.usuario == data.usuario, Usuario.id != current_user.id).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El nombre de usuario ya está registrado"
                )
            current_user.usuario = data.usuario.strip()

        if data.email is not None and data.email.strip() != "":
            # Verificar si ya existe el email
            existing = db.query(Usuario).filter(Usuario.email == data.email, Usuario.id != current_user.id).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El correo electrónico ya está registrado"
                )
            current_user.email = data.email.strip()

        if data.nombre_completo is not None and data.nombre_completo.strip() != "":
            current_user.nombre_completo = data.nombre_completo.strip()

        if data.password is not None and data.password.strip() != "":
            if len(data.password) < 6:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La contraseña debe tener al menos 6 caracteres"
                )
            current_user.password_hash = AuthService.get_password_hash(data.password)

        try:
            db.commit()
            db.refresh(current_user)
            return current_user
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar perfil: {str(e)}"
            )

