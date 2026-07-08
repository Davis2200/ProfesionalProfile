from fastapi import APIRouter, Depends, Request, BackgroundTasks, status
from supabase import Client
from ..schemas.contact import ContactSubmissionCreate, ContactSubmissionOut
from ..crud.contact import create_contact_submission
from ..services.resend import EmailService
from ..core.security import get_supabase
from ..core.rate_limit import contact_rate_limiter

router = APIRouter(prefix="/contact", tags=["Contact"])

@router.post(
    "/", 
    response_model=ContactSubmissionOut, 
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(contact_rate_limiter)]
)
async def submit_contact(
    request: Request,
    contact_in: ContactSubmissionCreate,
    background_tasks: BackgroundTasks,
    db: Client = Depends(get_supabase)
):
    """
    Procesa el formulario conversacional (RF-6.1).
    - Aplica Postel's Law en la normalización de datos.
    - Usa OAuth data si está presente para reducir la fricción.
    - Dispara un correo de agradecimiento asíncrono (Resend).
    """
    # 1. Persistencia en Supabase
    submission = await create_contact_submission(
        db, 
        contact_in, 
        client_ip=request.client.host
    )
    
    # 2. Notificación asíncrona (Peak-End Rule)
    # Se usa el email normalizado para el envío
    normalized_email = contact_in.raw_email.strip().lower()
    await EmailService.trigger_contact_notification(
        background_tasks, 
        email=normalized_email, 
        name=contact_in.raw_name
    )
    
    return submission