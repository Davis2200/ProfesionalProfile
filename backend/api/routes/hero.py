from fastapi import APIRouter
from ..schemas.content import HeroSectionOut

router = APIRouter(prefix="/hero", tags=["Content"])

@router.get("/", response_model=HeroSectionOut)
async def get_hero_config():
    """
    Retorna la configuración del Acto I: Génesis.
    Incluye los strings para el titular rotativo (RF-1.3).
    """
    return {
        "rotating_titles": [
            "Modelado Predictivo", 
            "Gobernanza de Datos", 
            "Desarrollo Full Stack"
        ],
        "aurora_config": {
            "base_color": "oklch(0.99 0.01 235)",
            "accent_color": "oklch(0.70 0.25 15)"
        }
    }
