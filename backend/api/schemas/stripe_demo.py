from pydantic import BaseModel, EmailStr
from typing import List

class ProductOut(BaseModel):
    id: str
    name: str
    price: float
    currency: str = "USD"

class CheckoutSessionCreate(BaseModel):
    product_ids: List[str]
    success_url: str
    cancel_url: str

class CheckoutSessionOut(BaseModel):
    checkout_url: str
    session_id: str