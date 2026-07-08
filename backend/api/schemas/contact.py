from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional

class ContactSubmissionCreate(BaseModel):
    # Postel's Law: Capturamos valores 'raw' para normalizarlos [3]
    raw_name: str = Field(..., min_length=2)
    raw_email: str
    message: str = Field(..., max_length=1000)
    
    # Soporte OAuth para evitar formularios manuales [10]
    oauth_provider: Optional[str] = None # 'github' o 'linkedin'
    oauth_subject: Optional[str] = None

class ContactSubmissionOut(BaseModel):
    id: str
    status: str = "received"
    message: str = "¡Gracias! Tu mensaje ha sido procesado con integridad [9]."
    
    model_config = ConfigDict(from_attributes=True)