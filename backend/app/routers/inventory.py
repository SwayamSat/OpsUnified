from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.routers import deps
from app.models.user import User
from app.models.forms_inventory import InventoryItem
from pydantic import BaseModel

router = APIRouter()

class InventoryItemCreate(BaseModel):
    name: str
    quantity: int
    low_stock_threshold: int = 5

@router.post("/")
def create_inventory_item(
    item_in: InventoryItemCreate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    item = InventoryItem(
        workspace_id=current_user.workspace_id,
        name=item_in.name,
        quantity=item_in.quantity,
        low_stock_threshold=item_in.low_stock_threshold
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/")
def list_inventory(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    return db.query(InventoryItem).filter(InventoryItem.workspace_id == current_user.workspace_id).all()
