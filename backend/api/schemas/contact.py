import datetime
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

# Este sí lo está encontrando
class ContactSubmissionCreate(BaseModel):
    name: str
    email: EmailStr
    message: str
    integrity_badge_version: UUID

# =============== ASEGÚRATE DE QUE ESTO EXISTA ==============
class ContactSubmissionOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    message: str
    created_at: datetime
    

    class Config:
        from_attributes = True  # O orm_mode = True si usas Pydantic v1