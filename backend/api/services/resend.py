import resend
from ..core.config import settings
from fastapi import BackgroundTasks

resend.api_key = settings.RESEND_API_KEY

class EmailService:
    @staticmethod
    def send_thank_you_email(to_email: str, name: str):
        """
        Envía un correo de agradecimiento personalizado.
        Diseñado para dejar una sensación de satisfacción (Peak-End Rule).
        """
        try:
            params = {
                "from": "David <portfolio@tu-dominio.com>",
                "to": [to_email],
                "subject": "Un mensaje desde The Tranquil Journey",
                "html": f"""
                    <h1>Hola, {name}</h1>
                    <p>Gracias por iniciar este vínculo humano.</p>
                    <p>He recibido tus datos con integridad y te contactaré pronto.</p>
                    <hr/>
                    <small>Este mensaje cumple con el Badge de Integridad v1.0</small>
                """
            }
            resend.Emails.send(params)
        except Exception as e:
            # En servicios de notificación, el error no debe romper el flujo principal
            print(f"Error enviando correo vía Resend: {e}")

    @classmethod
    async def trigger_contact_notification(
        cls, 
        background_tasks: BackgroundTasks, 
        email: str, 
        name: str
    ):
        """Dispara el correo en segundo plano para no aumentar el tiempo de respuesta de la API."""
        background_tasks.add_task(cls.send_thank_you_email, email, name)