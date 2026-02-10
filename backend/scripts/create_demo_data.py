import sys
import os
import random
from datetime import datetime, timedelta

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core import security
from app.models.user import User, UserRole
from app.models.workspace import Workspace
from app.models.operations import Service, Availability, Booking
from app.models.crm import Contact, Conversation, Message, MessageDirection
from app.models.forms_inventory import InventoryItem
from app.models.system import Alert

def create_demo_data():
    db = SessionLocal()
    try:
        print("Creating demo data...")
        
        # 1. Create Workspace
        ws = db.query(Workspace).filter(Workspace.contact_email == "demo@careops.com").first()
        if not ws:
            ws = Workspace(
                name="CareOps Demo Clinic",
                address="123 Health St, Tech City",
                timezone="UTC",
                contact_email="demo@careops.com",
                status="active",
                settings={"email": "mock_key", "sms": "mock_key"}
            )
            db.add(ws)
            db.commit()
            db.refresh(ws)
            print(f"Created Workspace: {ws.name}")
        
        # 2. Create Owner
        owner = db.query(User).filter(User.email == "demo@careops.com").first()
        if not owner:
            owner = User(
                email="demo@careops.com",
                password_hash=security.get_password_hash("demo123"),
                role=UserRole.OWNER,
                workspace_id=ws.id
            )
            db.add(owner)
            db.commit()
            print("Created Owner: demo@careops.com / demo123")
            
        # 3. Create Service
        svc = db.query(Service).filter(Service.name == "General Consultation", Service.workspace_id == ws.id).first()
        if not svc:
            svc = Service(
                workspace_id=ws.id,
                name="General Consultation",
                duration=30,
                location="Room 1"
            )
            db.add(svc)
            db.commit()
            db.refresh(svc)
            
            # Availability
            avail = Availability(
                service_id=svc.id,
                day_of_week=1, # Monday
                start_time="09:00",
                end_time="17:00"
            )
            db.add(avail)
            db.commit()
            print("Created Service: General Consultation")
            
        # 4. Create Inventory
        inv = db.query(InventoryItem).filter(InventoryItem.name == "Medical Kit", InventoryItem.workspace_id == ws.id).first()
        if not inv:
            inv = InventoryItem(
                workspace_id=ws.id,
                name="Medical Kit",
                quantity=10,
                low_stock_threshold=5
            )
            db.add(inv)
            db.commit()
            print("Created Inventory: Medical Kit")
            
        # 5. Create Contacts & Conversations
        contacts_data = [
            ("Alice Smith", "alice@example.com", "555-0101"),
            ("Bob Jones", "bob@example.com", "555-0102"),
            ("Charlie Brown", "charlie@example.com", "555-0103")
        ]
        
        for name, email, phone in contacts_data:
            contact = db.query(Contact).filter(Contact.email == email).first()
            if not contact:
                contact = Contact(workspace_id=ws.id, name=name, email=email, phone=phone)
                db.add(contact)
                db.commit()
                db.refresh(contact)
                
                # Conversation
                conv = Conversation(workspace_id=ws.id, contact_id=contact.id, status="active")
                db.add(conv)
                db.commit()
                db.refresh(conv)
                
                # Messages
                m1 = Message(
                    conversation_id=conv.id, 
                    direction=MessageDirection.INBOUND, 
                    type="email", 
                    content=f"Hi, I'm interested in a consultation. ({name})"
                )
                db.add(m1)
                
                # Auto-reply simulation
                m2 = Message(
                    conversation_id=conv.id,
                    direction=MessageDirection.OUTBOUND,
                    type="email",
                    content=f"Hi {name}, thanks for reaching out! You can book here: [Link]"
                )
                db.add(m2)
                db.commit()
                
        # 6. Create Bookings
        # Alice booked
        c_alice = db.query(Contact).filter(Contact.email == "alice@example.com").first()
        if c_alice:
            b = Booking(
                service_id=svc.id,
                contact_id=c_alice.id,
                start_time=datetime.now() + timedelta(days=1),
                end_time=datetime.now() + timedelta(days=1, minutes=30),
                status="confirmed"
            )
            db.add(b)
            db.commit()
            print("Created Booking for Alice")
            
        # 7. Low Stock Alert
        inv_low = InventoryItem(
            workspace_id=ws.id,
            name="Bandages",
            quantity=2,
            low_stock_threshold=5
        )
        db.add(inv_low)
        db.commit()
        
        alert = Alert(
            workspace_id=ws.id,
            type="inventory_low",
            message="Inventory item 'Bandages' is low (2 remaining)."
        )
        db.add(alert)
        db.commit()
        print("Created Low Stock Alert")

        print("Demo Data Generation Complete!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_demo_data()
