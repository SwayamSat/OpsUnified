from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.routers import deps
from app.models.user import User
from app.models.forms_inventory import FormTemplate
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()

class FormTemplateCreate(BaseModel):
    name: str
    schema: Dict[str, Any] # JSON schema

@router.post("/")
def create_form_template(
    form_in: FormTemplateCreate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    form = FormTemplate(
        workspace_id=current_user.workspace_id,
        name=form_in.name,
        schema=form_in.schema
    )
    db.add(form)
    db.commit()
    db.refresh(form)
    return form

@router.get("/")
def list_forms(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(FormTemplate).filter(FormTemplate.workspace_id == current_user.workspace_id).all()
