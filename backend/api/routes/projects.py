from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from typing import List
from supabase import Client
import stripe

from ..crud.projects import get_all_project_cards, get_project_by_slug
from ..schemas.project import ProjectCardOut, ProjectDeepDiveOut
from ..core.security import get_supabase

# Importas tus configuraciones y el servicio que ya creaste
from ..core.config import settings
from ..services.stripe import StripeService  # Ajusta la ruta de importación si es necesario
from ..schemas.stripe_demo import CheckoutSessionOut  # Asegúrate de importar tu esquema

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectCardOut])
async def read_projects(db: Client = Depends(get_supabase)):
    """Retorna el listado de tarjetas para la galería principal (RF-4.1)."""
    return await get_all_project_cards(db)


@router.get("/{slug}", response_model=ProjectDeepDiveOut)
async def read_project_detail(slug: str, db: Client = Depends(get_supabase)):
    """Proporciona los detalles del 'Deep Dive' (RF-4.3)."""
    project = await get_project_by_slug(db, slug)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Proyecto no encontrado en este viaje."
        )
    return project


# ==========================================
# NUEVO: ENDPOINT PARA CREAR LA SESIÓN DE PAGO (RF-4.4)
# ==========================================
@router.post("/checkout", response_model=CheckoutSessionOut)
async def create_checkout(items: List[dict], user_email: str):
    """
    Endpoint que consume tu StripeService para generar la URL de la pasarela.
    """
    return await StripeService.create_checkout_session(items, user_email)


# ==========================================
# NUEVO: ENDPOINT PARA EL WEBHOOK DE STRIPE
# ==========================================
@router.post("/webhook", status_code=status.HTTP_200_OK)
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    """
    Endpoint que escucha las notificaciones automáticas de Stripe.
    Valida la firma usando tu STRIPE_WEBHOOK_SECRET.
    """
    if not stripe_signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Falta la firma de Stripe"
        )
        
    try:
        # Stripe requiere los bytes crudos (raw body) para verificar la firma
        payload = await request.body()
        
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Payload inválido")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Verificación de firma fallida")

    # ---- PROCESAMIENTO DEL EVENTO ----
    event_type = event["type"]
    data_object = event["data"]["object"]

    if event_type == "checkout.session.completed":
        session = data_object
        customer_email = session.get("customer_details", {}).get("email")
        metadata = session.get("metadata", {})
        
        # TODO: Aquí ejecutas tus acciones post-pago
        # Ejemplo: Actualizar estado en tu DB de Supabase o enviar correo con Resend
        print(f"¡Pago confirmado vía Webhook para: {customer_email}!")

    return {"status": "success"}