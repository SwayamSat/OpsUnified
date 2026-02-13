from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.routers import deps
from app.models.user import User
from app.models.forms_inventory import AutomationRule, AutomationActionType, FormTemplate
from pydantic import BaseModel
from typing import Dict, Any, List

router = APIRouter()

class AutomationRuleCreate(BaseModel):
    name: str
    form_template_id: int
    action_type: AutomationActionType
    action_config: Dict[str, Any]
    is_active: int = 1

class AutomationRuleOut(AutomationRuleCreate):
    id: int
    workspace_id: int
    
    class Config:
        orm_mode = True

@router.post("/", response_model=AutomationRuleOut)
def create_automation_rule(
    rule_in: AutomationRuleCreate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Verify template belongs to workspace
    template = db.query(FormTemplate).filter(FormTemplate.id == rule_in.form_template_id, FormTemplate.workspace_id == current_user.workspace_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="Form template not found")

    rule = AutomationRule(
        workspace_id=current_user.workspace_id,
        name=rule_in.name,
        form_template_id=rule_in.form_template_id,
        action_type=rule_in.action_type,
        action_config=rule_in.action_config,
        is_active=rule_in.is_active
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule

@router.get("/", response_model=List[AutomationRuleOut])
def list_automation_rules(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(AutomationRule).filter(AutomationRule.workspace_id == current_user.workspace_id).all()

@router.delete("/{rule_id}")
def delete_automation_rule(
    rule_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    rule = db.query(AutomationRule).filter(AutomationRule.id == rule_id, AutomationRule.workspace_id == current_user.workspace_id).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    db.delete(rule)
    db.commit()
    return {"message": "Rule deleted"}
