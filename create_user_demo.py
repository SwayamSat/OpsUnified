import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core import security
from app.models.user import User, UserRole
from app.models.workspace import Workspace

def create_user_demo():
    db = SessionLocal()
    try:
        print("Creating User Demo Workspace...")
        
        # 1. Create Workspace
        ws_name = "My Demo Company"
        ws_email = "user@demo.com"
        
        ws = db.query(Workspace).filter(Workspace.contact_email == ws_email).first()
        if not ws:
            ws = Workspace(
                name=ws_name,
                address="456 Innovation Dr",
                timezone="UTC",
                contact_email=ws_email,
                status="active",
                settings={"email": "mock_key", "sms": "mock_key"}
            )
            db.add(ws)
            db.commit()
            db.refresh(ws)
            print(f"Created Workspace: {ws.name}")
        else:
            print(f"Workspace {ws.name} already exists.")
        
        # 2. Create Owner
        password = "password123"
        owner = db.query(User).filter(User.email == ws_email).first()
        if not owner:
            owner = User(
                email=ws_email,
                password_hash=security.get_password_hash(password),
                role=UserRole.OWNER,
                workspace_id=ws.id
            )
            db.add(owner)
            db.commit()
            print(f"Created Owner: {ws_email} / {password}")
        else:
             # Update password just in case
             owner.password_hash = security.get_password_hash(password)
             db.commit()
             print(f"Updated Owner Password: {ws_email} / {password}")
             
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_user_demo()
