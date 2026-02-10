from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.routers import deps
from app.models.user import User
from app.models.crm import Contact, Conversation
from app.models.operations import Booking
from app.models.forms_inventory import FormSubmission
from app.models.system import Alert

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    ws_id = current_user.workspace_id
    
    total_bookings = db.query(Booking).join(Booking.service).filter(Booking.service.has(workspace_id=ws_id)).count()
    total_contacts = db.query(Contact).filter(Contact.workspace_id == ws_id).count()
    active_conversations = db.query(Conversation).filter(Conversation.workspace_id == ws_id, Conversation.status == "active").count()
    pending_forms = db.query(FormSubmission).join(FormSubmission.template).filter(FormSubmission.template.has(workspace_id=ws_id), FormSubmission.status == "pending").count()
    
    alerts = db.query(Alert).filter(Alert.workspace_id == ws_id, Alert.is_read == False).all()
    
    return {
        "metrics": {
            "bookings": total_bookings,
            "contacts": total_contacts,
            "active_conversations": active_conversations,
            "pending_forms": pending_forms
        },
        "alerts": alerts
    }
