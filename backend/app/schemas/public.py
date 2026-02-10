from pydantic import BaseModel, EmailStr
from typing import Optional

class ContactFormSubmit(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    message: Optional[str] = None

class ContactResponse(BaseModel):
    id: int
    message: str
