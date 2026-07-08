from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class HeroSectionOut(BaseModel):
    rotating_titles: List[str] # "Modelado Predictivo", etc. [11]
    aurora_config: dict # Colores OKLCH específicos [7]

class IntegrityBadgeOut(BaseModel):
    version: str
    content_text: str # Explicación transparente del manejo de datos [9]
    last_updated: str

class AudioTrackOut(BaseModel):
    title: str
    artist: str
    stream_url: HttpUrl
    cover_url: Optional[HttpUrl]