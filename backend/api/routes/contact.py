from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks, status
from supabase import Client
from ..schemas.contact import ContactSubmissionCreate, ContactSubmissionOut
from ..crud.contact import create_contact_submission
from ..services.resend import EmailService
from ..db.sessions import supabase_service  # 👈 Importamos el cliente con bypass RLS
from ..core.rate_limit import contact_rate_limiter

router = APIRouter(prefix="/contact", tags=["Contact"])

# Dependencia local para inyectar explícitamente el cliente con privilegios Service Role
def get_service_db() -> Client:
    return supabase_service

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
    db: Client = Depends(get_service_db) # 👈 Ahora inyecta el cliente administrador
):
    
    # Verificación del Badge usando el cliente Service Role para saltar RLS
    badge_check = db.table("integrity_badges")\
        .select("*")\
        .eq("id", str(contact_in.integrity_badge_version))\
        .eq("is_active", True)\
        .single()\
        .execute()
    
    if not badge_check.data:
        raise HTTPException(status_code=400, detail="Versión de Badge de Integridad inválida o caducada.")
    
    """
    Procesa el formulario conversacional (RF-6.1).
    - Aplica Postel's Law en la normalización de datos.
    - Usa OAuth data si está presente para reducir la fricción.
    - Dispara un correo de agradecimiento asíncrono (Resend).
    """
    # 1. Persistencia en Supabase (Viaja con bypass RLS)
    submission = await create_contact_submission(
        db=db, 
        contact_in=contact_in, 
        client_ip=request.client.host if request.client else "127.0.0.1"
    )
    
    # 2. Notificación asíncrona (Peak-End Rule)
    # CORRECCIÓN: Leemos desde las propiedades limpias '.email' y '.name' de tu nuevo Pydantic
    normalized_email = contact_in.email.strip().lower()
    await EmailService.trigger_contact_notification(
        background_tasks, 
        email=normalized_email, 
        name=contact_in.name
    )
    
    return submission