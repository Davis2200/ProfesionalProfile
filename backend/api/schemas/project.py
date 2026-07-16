from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ProjectCardOut(BaseModel):
    title: str
    slug: str
    short_description: str  # mapeado desde projects.summary
    thumbnail_url: Optional[HttpUrl] = None  # mapeado desde projects.cover_image_url
    glass_intensity: float = 0.15  # Token de diseño UI/UX [7] - no existe en la BD, usa default
    tags: List[str] = []  # mapeado desde project_tech_stack.tech_name

class ProjectDeepDiveOut(ProjectCardOut):
    long_description: str  # mapeado desde projects.description_md
    architecture: Optional[str] = None  # mapeado desde projects.architecture_md
    results: Optional[str] = None  # mapeado desde projects.results_md