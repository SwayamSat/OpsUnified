from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core import security
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.token import Token

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    password = form_data.password
    if not password:
         raise HTTPException(status_code=400, detail="Password is required")
         
    # Try to find user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
    
@router.post("/setup-owner", response_model=Token)
def setup_owner(
    db: Session = Depends(get_db),
    email: str = "owner@example.com",
    password: str = "owner123"
) -> Any:
    # Check if any owner exists
    existing_owner = db.query(User).filter(User.role == UserRole.OWNER).first()
    if existing_owner:
         raise HTTPException(status_code=400, detail="Owner already exists")
         
    # Create owner
    # Note: We need a workspace first, but for now we'll create user.
    # Actually User needs workspace_id. So we need to create workspace too if not exists.
    # This might be part of Step 1: Workspace Creation.
    # But for "setup" let's assume this is a dev helper for now or just creates user without workspace?
    # No, constraint says User needs workspace_id.
    
    # We will defer this to the Workspace Creation step.
    pass

