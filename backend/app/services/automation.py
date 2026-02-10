from sqlalchemy.orm import Session
from app.core import events
from app.core.database import SessionLocal
from app.models.crm import Contact, Conversation, Message, MessageDirection, MessageType
from app.models.operations import Booking, Service
from app.models.system import Alert
from app.models.workspace import Workspace
from app.models.forms_inventory import InventoryItem
from typing import Dict, Any

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Actions
def send_welcome_message(payload: Dict[str, Any]):
    db = SessionLocal()
    try:
        contact_id = payload.get("contact_id")
        workspace_id = payload.get("workspace_id")
        
        # Logic: Find contact, create conversation if needed, send message
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if not contact: return

        # Simple welcome message
        content = f"Hi {contact.name}, thanks for reaching out! How can we help you today?"
        
        # Check for existing active conversation
        conversation = db.query(Conversation).filter(Conversation.contact_id == contact_id).first()
        if not conversation:
            conversation = Conversation(workspace_id=workspace_id, contact_id=contact_id, status="active")
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            
        msg = Message(
            conversation_id=conversation.id,
            direction=MessageDirection.OUTBOUND,
            type=MessageType.SMS if contact.phone else MessageType.EMAIL,
            content=content
        )
        db.add(msg)
        db.commit()
        print(f"[AUTOMATION] Sent welcome message to {contact.email or contact.phone}")
    finally:
        db.close()

def handle_booking_created(payload: Dict[str, Any]):
    db = SessionLocal()
    try:
        booking_id = payload.get("booking_id")
        booking = db.query(Booking).filter(Booking.id == booking_id).first()
        if not booking: return
        
        # 1. Send Confirmation
        msg_content = f"Booking confirmed for {booking.service.name} at {booking.start_time}."
        
        # Find conversation
        conversation = db.query(Conversation).filter(Conversation.contact_id == booking.contact_id).first()
        if conversation:
            msg = Message(
                conversation_id=conversation.id,
                direction=MessageDirection.OUTBOUND,
                type=MessageType.SYSTEM,
                content=msg_content
            )
            db.add(msg)
            db.commit()
            print(f"[AUTOMATION] Sent booking confirmation to Contact {booking.contact_id}")
            
        # 2. Schedule Forms (Mock: just Log it)
        print(f"[AUTOMATION] Scheduled post-booking forms for Booking {booking.id}")

    finally:
        db.close()

def handle_inventory_low(payload: Dict[str, Any]):
    db = SessionLocal()
    try:
        item_id = payload.get("item_id")
        item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
        if not item: return
        
        alert = Alert(
            workspace_id=item.workspace_id,
            type="inventory_low",
            message=f"Inventory item '{item.name}' is low ({item.quantity} remaining)."
        )
        db.add(alert)
        db.commit()
        print(f"[AUTOMATION] Created Low Stock Alert for {item.name}")
    finally:
        db.close()

def start_automation():
    print("[AUTOMATION] Starting Automation Engine...")
    events.subscribe(events.NEW_CONTACT, send_welcome_message)
    events.subscribe(events.BOOKING_CREATED, handle_booking_created)
    events.subscribe(events.INVENTORY_LOW, handle_inventory_low)
