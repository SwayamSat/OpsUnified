from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class WorkspaceStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"

class WorkspaceBase(BaseModel):
    name: str
    address: Optional[str] = None
    timezone: str = "UTC"
    contact_email: EmailStr

class WorkspaceCreate(WorkspaceBase):
    owner_email: EmailStr
    owner_password: str

class Workspace(WorkspaceBase):
    id: int
    status: WorkspaceStatus
    
    class Config:
        from_attributes = True
