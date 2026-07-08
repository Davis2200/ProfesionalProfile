from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ProjectCardOut(BaseModel):
    title: str
    slug: str
    short_description: str
    thumbnail_url: HttpUrl
    glass_intensity: float = 0.15 # Token de diseño UI/UX [7]

class ProjectDeepDiveOut(ProjectCardOut):
    long_description: str
    stack: List[str]
    architecture_diagram_url: Optional[HttpUrl]
    key_results: List[str] # Resultados medibles [8]
    github_url: Optional[HttpUrl]
    live_demo_url: Optional[HttpUrl]