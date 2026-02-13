from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.routers import deps
from app.models.user import User
from app.models.forms_inventory import InventoryItem, InventoryUsage
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
    return db.query(InventoryItem).filter(InventoryItem.workspace_id == current_user.workspace_id).all() # Should order by name?

class InventoryUsageCreate(BaseModel):
    item_id: int
    quantity_used: int
    booking_id: int = None # Optional linking

@router.post("/usage")
def record_usage(
    usage_in: InventoryUsageCreate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    item = db.query(InventoryItem).filter(InventoryItem.id == usage_in.item_id, InventoryItem.workspace_id == current_user.workspace_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    # Check quantity
    if item.quantity < usage_in.quantity_used:
        raise HTTPException(status_code=400, detail="Insufficient quantity")

    item.quantity -= usage_in.quantity_used
    
    if usage_in.booking_id:
        from app.models.forms_inventory import InventoryUsage
        usage = InventoryUsage(
            booking_id=usage_in.booking_id,
            item_id=item.id,
            quantity_used=usage_in.quantity_used
        )
        db.add(usage)
    
    db.commit()
    db.refresh(item)
    return item

@router.put("/{item_id}")
def update_inventory_item(
    item_id: int,
    item_in: InventoryItemCreate,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id, InventoryItem.workspace_id == current_user.workspace_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    item.name = item_in.name
    item.quantity = item_in.quantity
    item.low_stock_threshold = item_in.low_stock_threshold
    
    db.commit()
    db.refresh(item)
    return item
