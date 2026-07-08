from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import Client
from ..crud.projects import get_all_project_cards, get_project_by_slug
from ..schemas.project import ProjectCardOut, ProjectDeepDiveOut
from ..core.security import get_supabase

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=List[ProjectCardOut])
async def read_projects(db: Client = Depends(get_supabase)):
    """Retorna el listado de tarjetas para la galería principal (RF-4.1)."""
    return await get_all_project_cards(db)

@router.get("/{slug}", response_model=ProjectDeepDiveOut)
async def read_project_detail(slug: str, db: Client = Depends(get_supabase)):
    """
    Proporciona los detalles del 'Deep Dive' (RF-4.3).
    Si el proyecto no existe, lanza un error 404.
    """
    project = await get_project_by_slug(db, slug)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Proyecto no encontrado en este viaje."
        )
    return project