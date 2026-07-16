from fastapi import APIRouter, Depends
from supabase import Client
from ..core.security import get_supabase
from ..schemas.integrityBadge import IntegrityBadgeOut
from ..crud.integrityBadge import get_active_integrity_badge

router = APIRouter(prefix="/integrity-badge", tags=["Governance"])

@router.get("/", response_model=IntegrityBadgeOut)
async def read_active_badge(db: Client = Depends(get_supabase)):
    """
    Entrega el contenido y la versión actual del Badge de Integridad.
    El frontend debe almacenar el ID para enviarlo en el formulario de contacto.
    """
    return await get_active_integrity_badge(db)