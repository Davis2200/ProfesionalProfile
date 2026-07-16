from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class IntegrityBadgeOut(BaseModel):
    """Contrato para la carga dinámica del Badge de Integridad (RF-6.5)"""
    id: UUID = Field(..., description="Identificador único para trazabilidad legal")
    version: str = Field(..., example="1.1.0")
    content: str = Field(..., description="Texto legal que el usuario debe visualizar")
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }