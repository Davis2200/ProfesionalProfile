from supabase import Client
from ..schemas.integrityBadge import IntegrityBadgeOut

async def get_active_integrity_badge(db: Client) -> IntegrityBadgeOut:
    """Recupera la política de integridad activa para el frontend (Gobernanza Dinámica)"""
    response = db.table("integrity_badges")\
        .select("*")\
        .eq("is_active", True)\
        .single()\
        .execute()
    
    return IntegrityBadgeOut(**response.data)