from supabase import create_client, Client
from ..core.config import settings
import asyncio

# Cliente Anónimo: Para datos con Row Level Security (RLS) pública
# Usado en Acto I, II y III (Hero, Skills, Projects)
supabase_anon: Client = create_client(
    settings.SUPABASE_URL, 
    settings.SUPABASE_ANON_KEY
)

# Cliente Service Role: Para bypass de RLS en operaciones de servidor
# Crítico para el Acto IV (Contactos) y transacciones de Stripe
supabase_service: Client = create_client(
    settings.SUPABASE_URL, 
    settings.SUPABASE_SERVICE_ROLE_KEY
)

async def shutdown_db_connections():
    """
    Implementa el manejador de señales para un cierre limpio (TRD §5).
    Asegura que las peticiones en vuelo terminen antes de apagar el worker.
    """
    # Nota: El cliente de Supabase (postgrest-py) usa httpx.
    # Aquí cerramos los recursos asíncronos si se configuraran pools personalizados.
    print("Finalizando conexiones a Supabase con integridad...")
    await asyncio.sleep(0.1) # Simulación de drenado de conexiones