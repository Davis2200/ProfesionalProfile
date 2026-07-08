from typing import Generator
from supabase import Client
from .sessions import supabase_anon, supabase_service

def get_db_anon() -> Generator[Client, None, None]:
    """
    Dependencia para obtener el cliente anónimo.
    Ideal para rutas de solo lectura como el Bento Box (RF-3.1).
    """
    try:
        yield supabase_anon
    finally:
        # La limpieza se gestiona en sessions.py (Graceful Shutdown)
        pass

def get_db_service() -> Generator[Client, None, None]:
    """
    Dependencia para obtener el cliente con privilegios de servicio.
    Debe usarse con cautela, solo en lógica de servidor (Stripe/Contactos).
    Refuerza la Seguridad (TRD §1) al no exponer el key al navegador.
    """
    try:
        yield supabase_service
    finally:
        pass