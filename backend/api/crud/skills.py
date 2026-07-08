from supabase import Client
from typing import List
from ..schemas.skill import SkillOut, SkillBlockOut

async def get_skills_grouped(db: Client) -> List[SkillBlockOut]:
    """
    Recupera las habilidades organizadas por categorías para el Bento Box.
    Refuerza la Ley de Miller filtrando el contenido para no exceder 
    la capacidad cognitiva del visitante [3].
    """
    # Consulta a la tabla 'skills' en Supabase
    response = db.table("skills").select("*").order("proficiency_level", desc=True).execute()
    skills_data = response.data

    # Agrupación por categorías (Dominio)
    categories = sorted(list(set(s["category"] for s in skills_data)))
    grouped_skills = []

    for cat in categories:
        items = [SkillOut(**s) for s in skills_data if s["category"] == cat]
        # Solo agregamos el bloque si tiene sentido visual (máximo 9 items)
        grouped_skills.append(
            SkillBlockOut(block_title=cat, items=items[:9])
        )

    return grouped_skills