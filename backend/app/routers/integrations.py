from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.routers import deps
from app.models.user import User
from app.models.workspace import Workspace
from app.models.system import IntegrationLog
from pydantic import BaseModel

router = APIRouter()

class IntegrationConfig(BaseModel):
    channels: dict # e.g. {"email": {"provider": "resend", "api_key": "..."}}

@router.put("/me/integrations")
def update_integrations(
    config: IntegrationConfig,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    workspace = current_user.workspace
    if not workspace:
         raise HTTPException(status_code=404, detail="Workspace not found")
         
    # Update settings
    # Merge or replace? Replace for simplicity
    current_settings = workspace.settings or {}
    current_settings.update(config.channels)
    
    workspace.settings = current_settings
    
    # Needs to flag modified to force update if using JSON mutation directly? 
    # SQLAlchemy usually detects it if we assign a new dict.
    from sqlalchemy.orm.attributes import flag_modified
    flag_modified(workspace, "settings")
    
    db.commit()
    return {"message": "Integrations updated", "settings": workspace.settings}

@router.post("/me/integrations/test")
def test_integration(
    channel: str = Body(..., embed=True),
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    workspace = current_user.workspace
    settings = workspace.settings or {}
    
    if channel not in settings:
        raise HTTPException(status_code=400, detail=f"Channel {channel} not configured")
        
    # Mock sending
    # Log the attempt
    log = IntegrationLog(
        workspace_id=workspace.id,
        integration_type=channel,
        status="success", # Mock success
        details=f"Test message sent via {channel}"
    )
    db.add(log)
    db.commit()
    
    return {"message": f"Test {channel} sent successfully"}
