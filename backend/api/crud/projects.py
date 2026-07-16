from supabase import Client
from typing import List, Optional
from ..schemas.project import ProjectCardOut, ProjectDeepDiveOut


def _extract_tags(row: dict) -> List[str]:
    """
    La tabla project_tech_stack guarda el stack técnico en filas separadas
    (relación 1-a-muchos con projects). Supabase las devuelve embebidas como
    una lista de dicts cuando se pide en el select; aquí las aplanamos a
    una simple lista de nombres para el frontend.
    """
    return [item["tech_name"] for item in (row.get("project_tech_stack") or [])]


async def get_all_project_cards(db: Client) -> List[ProjectCardOut]:
    """
    Retorna solo la información necesaria para renderizar las tarjetas iniciales.
    Esto ayuda a mantener un LCP bajo y una carga progresiva eficiente [6].
    """
    response = (
        db.table("projects")
        .select("title, slug, summary, cover_image_url, project_tech_stack(tech_name)")
        .eq("is_published", True)
        .order("display_order")
        .execute()
    )

    return [
        ProjectCardOut(
            title=p["title"],
            slug=p["slug"],
            short_description=p["summary"],
            thumbnail_url=p["cover_image_url"],
            tags=_extract_tags(p),
        )
        for p in response.data
    ]


async def get_project_by_slug(db: Client, slug: str) -> Optional[ProjectDeepDiveOut]:
    """
    Recupera la información completa para el modal de 'Deep Dive'.
    Incluye stack técnico y resultados medibles para validación técnica [4, 7].
    """
    response = (
        db.table("projects")
        .select(
            "title, slug, summary, description_md, architecture_md, results_md, "
            "cover_image_url, project_tech_stack(tech_name)"
        )
        .eq("slug", slug)
        .eq("is_published", True)
        .maybe_single()
        .execute()
    )

    if not response or not response.data:
        return None

    p = response.data
    return ProjectDeepDiveOut(
        title=p["title"],
        slug=p["slug"],
        short_description=p["summary"],
        thumbnail_url=p["cover_image_url"],
        long_description=p["description_md"],
        architecture=p.get("architecture_md"),
        results=p.get("results_md"),
        tags=_extract_tags(p),
    )