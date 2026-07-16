from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import Client
from ..crud.skills import get_skills_grouped
from ..schemas.skill import SkillBlockOut
from ..core.security import get_supabase

router = APIRouter(prefix="/skills", tags=["Skills"])

@router.get("/", response_model=List[SkillBlockOut])
async def read_skills(db: Client = Depends(get_supabase)):
    """
    Recupera las habilidades organizadas para el Bento Box (RF-3.1).
    Aplica Miller's Law para prevenir la sobrecarga de información.
    """
    return await get_skills_grouped(db)