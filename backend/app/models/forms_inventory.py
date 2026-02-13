from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class FormStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    OVERDUE = "overdue"

class FormTemplate(Base):
    __tablename__ = "form_templates"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    name = Column(String, nullable=False)
    schema = Column(JSON, nullable=False) # JSON schema for the form fields

    workspace = relationship("Workspace", back_populates="form_templates")
    submissions = relationship("FormSubmission", back_populates="template")
    automation_rules = relationship("AutomationRule", back_populates="form_template")

class FormSubmission(Base):
    __tablename__ = "form_submissions"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("form_templates.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    data = Column(JSON, nullable=True)
    status = Column(Enum(FormStatus), default=FormStatus.PENDING)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    due_at = Column(DateTime(timezone=True), nullable=True)

    template = relationship("FormTemplate", back_populates="submissions")
    contact = relationship("Contact", back_populates="form_submissions")

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    low_stock_threshold = Column(Integer, default=5)

    workspace = relationship("Workspace", back_populates="inventory_items")
    usages = relationship("InventoryUsage", back_populates="item")

class InventoryUsage(Base):
    __tablename__ = "inventory_usage"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    quantity_used = Column(Integer, nullable=False)

    booking = relationship("Booking", back_populates="inventory_usage")
    item = relationship("InventoryItem", back_populates="usages")

class AutomationActionType(str, enum.Enum):
    SEND_EMAIL = "send_email"
    SEND_SMS = "send_sms"

class AutomationRule(Base):
    __tablename__ = "automation_rules"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    form_template_id = Column(Integer, ForeignKey("form_templates.id"), nullable=True) # If null, could be global or other triggers
    name = Column(String, nullable=False)
    action_type = Column(Enum(AutomationActionType), nullable=False)
    action_config = Column(JSON, nullable=False) # { "recipient": "user@example.com", "template": "..." }
    is_active = Column(Integer, default=1) # 1=active, 0=inactive (using Integer for boolean compatibility if needed, else Boolean)

    workspace = relationship("Workspace", back_populates="automation_rules")
    form_template = relationship("FormTemplate", back_populates="automation_rules")
