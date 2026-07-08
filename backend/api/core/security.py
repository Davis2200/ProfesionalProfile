from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from supabase import create_client, Client
from .config import settings

# El token vendrá del frontend (Next.js) tras el login con GitHub/LinkedIn
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Cliente de Supabase inyectable (DI)
def get_supabase() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    supabase: Client = Depends(get_supabase)
):
    """
    Valida el JWT emitido por Supabase. 
    Esencial para el Acto IV para identificar al usuario sin fricción [2].
    """
    try:
        user = supabase.auth.get_user(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de autenticación inválido",
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error al validar identidad",
        )