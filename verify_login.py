import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.core import security

def verify_login(email, password):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"User {email} not found in database.")
            return
        
        print(f"User found: {user.email}, Role: {user.role}")
        print(f"Hashed Password in DB: {user.password_hash}")
        
        is_valid = security.verify_password(password, user.password_hash)
        if is_valid:
            print("SUCCESS: Password verified correctly!")
        else:
            print("FAILURE: Password verification failed.")
            
            # Debug: Hash the input password and compare
            new_hash = security.get_password_hash(password)
            print(f"Hash of input '{password}': {new_hash}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_login("demo@careops.com", "demo123")
