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

class FormSubmissionCreate(BaseModel):
    data: dict # Dynamic fields based on template schema
    contact_email: Optional[EmailStr] = None # To link to contact if provided
    contact_phone: Optional[str] = None
