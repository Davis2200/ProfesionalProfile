from supabase import Client
from typing import List
from ..schemas.skill import SkillOut, SkillBlockOut

async def get_skills_grouped(db: Client) -> List[SkillBlockOut]:
    """
    Recupera las habilidades organizadas por categorías para el Bento Box.
    Ajustado estrictamente para cumplir con las restricciones de 'skill.py' 
    y la base de datos relacional de Supabase.
    """
    # 1. Consultamos la tabla contenedora e incluimos sus habilidades hijas
    response = db.table("skill_blocks").select("*, skills(*)").order("display_order").execute()
    blocks_data = response.data

    grouped_skills = []

    for block in blocks_data:
        raw_skills = block.get("skills", [])
        # Ordenamos las habilidades internas según su display_order
        sorted_skills = sorted(raw_skills, key=lambda x: x.get("display_order", 0))

        items = []
        for s in sorted_skills:
            # Resolvemos los requerimientos obligatorios de SkillOut y SkillBase:
            items.append(
                SkillOut(
                    # Nota: Si tu Pydantic exige 'id: int', tendrás que castearlo provisionalmente 
                    # o cambiar tu esquema a 'str / UUID'. Si Supabase te da un UUID string, 
                    # aquí usamos un hash entero para que Pydantic no truene:
                    id=hash(s["id"]) & 0x7FFFFFFF, 
                    name=s["name"],
                    category=str(block["category"]), # Inyectamos la categoría del bloque padre
                    icon_svg_path=block.get("icon_key") or "default-icon", # Mapeamos al token del padre
                    proficiency_level=s.get("proficiency_level") or int(s.get("proficiency", 1) * 20) 
                    # El ge=1, le=100 de tu Pydantic se cumple multiplicando tu proficiency (1-5) * 20
                )
            )

        # 2. Construimos el bloque usando 'block_title' exactamente como lo pide tu SkillBlockOut
        grouped_skills.append(
            SkillBlockOut(
                block_title=block["title"], 
                items=items[:9]            
            )
        )

    return grouped_skills