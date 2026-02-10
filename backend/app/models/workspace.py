from sqlalchemy import Column, Integer, String, Enum, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class WorkspaceStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"

class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    timezone = Column(String, default="UTC")
    contact_email = Column(String, nullable=False)
    status = Column(Enum(WorkspaceStatus), default=WorkspaceStatus.DRAFT)
    settings = Column(JSON, nullable=True) # For storing integration config (Twilio/Resend keys)

    users = relationship("User", back_populates="workspace")
    contacts = relationship("Contact", back_populates="workspace")
    services = relationship("Service", back_populates="workspace")
    form_templates = relationship("FormTemplate", back_populates="workspace")
    inventory_items = relationship("InventoryItem", back_populates="workspace")
    alerts = relationship("Alert", back_populates="workspace")
