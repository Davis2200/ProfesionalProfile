from fastapi import APIRouter, HTTPException
from supabase import create_client, Client
from ..core.config import settings

router = APIRouter(prefix="/tracks", tags=["Audio Tracks"])

# Usa el nombre exacto que está definido en tu clase Settings
supabase: Client = create_client(
    settings.SUPABASE_URL, 
    settings.SUPABASE_SERVICE_ROLE_KEY
)

@router.get("/")
async def get_audio_tracks():
    try:
        response = supabase.table("audio_tracks").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))