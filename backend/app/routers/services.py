from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.routers import deps
from app.models.user import User
from app.models.operations import Service, Availability
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class AvailabilityCreate(BaseModel):
    day_of_week: int
    start_time: str
    end_time: str

class ServiceCreate(BaseModel):
    name: str
    duration: int
    location: Optional[str] = None
    availabilities: List[AvailabilityCreate]

@router.post("/")
def create_service(
    service_in: ServiceCreate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    workspace = current_user.workspace
    
    service = Service(
        workspace_id=workspace.id,
        name=service_in.name,
        duration=service_in.duration,
        location=service_in.location
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    
    for avail in service_in.availabilities:
        db_avail = Availability(
            service_id=service.id,
            day_of_week=avail.day_of_week,
            start_time=avail.start_time,
            end_time=avail.end_time
        )
        db.add(db_avail)
    
    db.commit()
    return service

@router.get("/")
def list_services(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(Service).filter(Service.workspace_id == current_user.workspace_id).all()
