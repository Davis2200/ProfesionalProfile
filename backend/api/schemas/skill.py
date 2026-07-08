from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class SkillBase(BaseModel):
    name: str = Field(..., example="DBSCAN")
    category: str = Field(..., example="Predictive Modeling")
    icon_svg_path: str
    proficiency_level: int = Field(ge=1, le=100)

class SkillOut(SkillBase):
    id: int
    
class SkillBlockOut(BaseModel):
    """Refuerza la Ley de Miller: Máximo 9 items por bloque visible [3]"""
    block_title: str
    items: List[SkillOut]

    @field_validator('items')
    @classmethod
    def enforce_millers_law(cls, v):
        if len(v) > 9:
            raise ValueError("Demasiados elementos. La carga cognitiva debe ser baja (Máx 9) [4].")
        return v