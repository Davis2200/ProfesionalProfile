from supabase import Client
from typing import List, Optional
from ..schemas.project import ProjectCardOut, ProjectDeepDiveOut

async def get_all_project_cards(db: Client) -> List[ProjectCardOut]:
    """
    Retorna solo la información necesaria para renderizar las tarjetas iniciales.
    Esto ayuda a mantener un LCP bajo y una carga progresiva eficiente [6].
    """
    response = db.table("projects").select(
        "title, slug, short_description, thumbnail_url, glass_intensity"
    ).execute()
    return [ProjectCardOut(**p) for p in response.data]

async def get_project_by_slug(db: Client, slug: str) -> Optional[ProjectDeepDiveOut]:
    """
    Recupera la información completa para el modal de 'Deep Dive'.
    Incluye stack técnico y resultados medibles para validación técnica [4, 7].
    """
    response = db.table("projects").select("*").eq("slug", slug).single().execute()
    if not response.data:
        return None
    return ProjectDeepDiveOut(**response.data)