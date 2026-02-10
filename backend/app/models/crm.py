from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class MessageDirection(str, enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

class MessageType(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    SYSTEM = "system"

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, index=True, nullable=True) # Allow null if only phone is provided? Standard says email/phone.
    phone = Column(String, index=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    workspace = relationship("Workspace", back_populates="contacts")
    conversations = relationship("Conversation", back_populates="contact")
    bookings = relationship("Booking", back_populates="contact")
    form_submissions = relationship("FormSubmission", back_populates="contact")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    status = Column(String, default="active") # active, paused (if staff reply)
    last_message_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    contact = relationship("Contact", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    direction = Column(Enum(MessageDirection), nullable=False)
    type = Column(Enum(MessageType), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")
