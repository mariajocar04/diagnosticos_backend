# diagnosticos_backend

Backend FastAPI para TICOS NurseDx.

## Requisitos

- Python 3.10+
- MySQL

## Instalacion

```bash
pip install -r requirements.txt
```

## Configuracion

Definir `DATABASE_URL` en el entorno con formato SQLAlchemy para MySQL, por ejemplo:

```bash
mysql+mysqlconnector://usuario:password@host:puerto/nombre_bd
```

Para OTP por correo, configurar tambien:

- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `MAIL_FROM`
- `MAIL_PORT`
- `MAIL_SERVER`
- `MAIL_FROM_NAME`
- `MAIL_STARTTLS`
- `MAIL_SSL_TLS`

## Actualizacion de BD (sin Alembic)

```bash
python scripts/db_update_remisiones.py
python seed_remisiones.py
```

## Ejecutar

```bash
python main.py
```

## Endpoints nuevos Dia 5

- `POST /api/v1/remisiones`
- `GET /api/v1/remisiones`
- `GET /api/v1/remisiones/{remision_id}`
- `PUT /api/v1/remisiones/{remision_id}`
- `POST /api/v1/remisiones/{remision_id}/estado`

- `POST /api/v1/auth/otp/request`
- `POST /api/v1/auth/otp/verify`
- `POST /api/v1/auth/password/reset`