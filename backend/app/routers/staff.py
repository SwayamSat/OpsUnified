from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.routers import deps
from app.core import security
from app.models.user import User, UserRole
from pydantic import BaseModel, EmailStr

router = APIRouter()

class StaffInvite(BaseModel):
    email: EmailStr
    password: str # In real app, would send invite link. Here we set password directly.

@router.post("/")
def invite_staff(
    invite: StaffInvite,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Only owner can invite
    if current_user.role != UserRole.OWNER:
        raise HTTPException(status_code=403, detail="Only owners can invite staff")
        
    # Check if user exists
    existing_user = db.query(User).filter(User.email == invite.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
        
    user = User(
        email=invite.email,
        password_hash=security.get_password_hash(invite.password),
        role=UserRole.STAFF,
        workspace_id=current_user.workspace_id
    )
    db.add(user)
    db.commit()
    return {"message": "Staff invited successfully", "email": user.email}

@router.get("/")
def list_staff(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(User).filter(
        User.workspace_id == current_user.workspace_id,
        User.role == UserRole.STAFF
    ).all()
