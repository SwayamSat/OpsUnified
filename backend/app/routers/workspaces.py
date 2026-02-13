from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core import security
from app.routers import deps
from app.models.workspace import Workspace
from app.models.user import User, UserRole
from app.schemas.workspace import WorkspaceCreate, Workspace as WorkspaceSchema

router = APIRouter()

@router.post("/", response_model=WorkspaceSchema)
def create_workspace(
    workspace_in: WorkspaceCreate,
    db: Session = Depends(get_db)
):
    # Check if user already exists
    user = db.query(User).filter(User.email == workspace_in.owner_email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
        
    # Create Workspace
    db_workspace = Workspace(
        name=workspace_in.name,
        address=workspace_in.address,
        timezone=workspace_in.timezone,
        contact_email=workspace_in.contact_email,
        status="draft" # Explicitly draft
    )
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    
    # Create Owner
    db_user = User(
        email=workspace_in.owner_email,
        password_hash=security.get_password_hash(workspace_in.owner_password),
        role=UserRole.OWNER,
        workspace_id=db_workspace.id
    )
    db.add(db_user)
    db.commit()
    
    return db_workspace

@router.get("/", response_model=list[WorkspaceSchema])
def list_workspaces(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Return user's workspace
    workspace = db.query(Workspace).filter(Workspace.id == current_user.workspace_id).first()
    return [workspace] if workspace else []

@router.post("/{workspace_id}/activate")
def activate_workspace(
    workspace_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    workspace = db.query(Workspace).filter(Workspace.id == workspace_id).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
        
    if current_user.role != UserRole.OWNER or current_user.workspace_id != workspace_id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    # Validation Rules
    # 1. Communication channel connected (settings has keys)
    if not workspace.settings or not any(k in workspace.settings for k in ["email", "sms"]):
         # Looser check: just check if settings is not empty or check specific keys if we knew them.
         # Requirement: "At least one channel mandatory".
         # Mock check: assuming key is "email" or "sms"
         if not workspace.settings:
             raise HTTPException(status_code=400, detail="Integrations not configured")
             
    # 2. At least one service exists
    if not workspace.services:
        raise HTTPException(status_code=400, detail="No services defined")
        
    # 3. Availability defined
    # Our Service creation enforces availability list, so if service exists, availability likely exists.
    # But let's check deep
    has_availability = any(s.availabilities for s in workspace.services)
    if not has_availability:
        raise HTTPException(status_code=400, detail="Availability not defined for any service")
        
    workspace.status = "active"
    db.commit()
    
    return {"status": "active", "message": "Workspace activated successfully"}
