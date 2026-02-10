from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class BookingStatus(str, enum.Enum):
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    CANCELLED = "cancelled"

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    name = Column(String, nullable=False)
    duration = Column(Integer, nullable=False) # In minutes
    location = Column(String, nullable=True)

    workspace = relationship("Workspace", back_populates="services")
    availabilities = relationship("Availability", back_populates="service")
    bookings = relationship("Booking", back_populates="service")

class Availability(Base):
    __tablename__ = "availabilities"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False) # 0=Monday, 6=Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    service = relationship("Service", back_populates="availabilities")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False) 
    status = Column(Enum(BookingStatus), default=BookingStatus.CONFIRMED)
    
    service = relationship("Service", back_populates="bookings")
    contact = relationship("Contact", back_populates="bookings")
    inventory_usage = relationship("InventoryUsage", back_populates="booking")
