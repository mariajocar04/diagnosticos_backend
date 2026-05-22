# coding=utf-8
import os
from pathlib import Path
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType


class EmailService:
    @staticmethod
    def _bool_env(name: str, default: bool) -> bool:
        value = os.getenv(name)
        if value is None:
            return default
        return value.strip().lower() in {"1", "true", "yes", "on"}

    @staticmethod
    def get_mail_config() -> ConnectionConfig:
        
        return ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
            MAIL_FROM=os.getenv("MAIL_FROM", ""),
            MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
            MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
            MAIL_STARTTLS=EmailService._bool_env("MAIL_STARTTLS", True),
            MAIL_SSL_TLS=EmailService._bool_env("MAIL_SSL_TLS", False),
            MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME", "TICOS NurseDx"),
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )

    @staticmethod
    def render_otp_html(otp_code: str) -> str:
        template_path = Path(__file__).resolve().parent.parent / "templates" / "email" / "otp.html"
        if template_path.exists():
            template = template_path.read_text(encoding="utf-8")
            return template.replace("{{OTP_CODE}}", otp_code)

        return (
            "<h2>Codigo OTP de recuperacion</h2>"
            f"<p>Tu codigo es: <b>{otp_code}</b></p>"
            "<p>Este codigo expira en 15 minutos.</p>"
        )

    @staticmethod
    async def send_otp_email(recipient_email: str, otp_code: str) -> None:
        conf = EmailService.get_mail_config()
        fm = FastMail(conf)
        message = MessageSchema(
            subject="TICOS NurseDx - Codigo OTP para cambiar contrasena",
            recipients=[recipient_email],
            body=EmailService.render_otp_html(otp_code),
            subtype=MessageType.html,
        )
        await fm.send_message(message)
