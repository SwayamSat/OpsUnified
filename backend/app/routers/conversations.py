from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.routers import deps
from app.models.user import User
from app.models.crm import Conversation, Message, MessageDirection, MessageType
from app.core import events
from pydantic import BaseModel

router = APIRouter()

class MessageCreate(BaseModel):
    content: str
    type: str = "email" # or sms

@router.get("/")
def list_conversations(
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    # Return all conversations for workspace
    return db.query(Conversation).filter(Conversation.workspace_id == current_user.workspace_id).all()

@router.get("/{conversation_id}/messages")
def get_messages(
    conversation_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.workspace_id == current_user.workspace_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation.messages

@router.post("/{conversation_id}/messages")
def reply_to_conversation(
    conversation_id: int,
    message_in: MessageCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(get_db)
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id, Conversation.workspace_id == current_user.workspace_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    # Create Message
    msg = Message(
        conversation_id=conversation.id,
        direction=MessageDirection.OUTBOUND,
        type=message_in.type,
        content=message_in.content
    )
    db.add(msg)
    
    # Logic: Staff reply pauses automation
    if conversation.status != "paused":
        conversation.status = "paused"
        print(f"[AUTOMATION] Paused automation for Conversation {conversation.id} due to STAFF_REPLY")
        background_tasks.add_task(events.emit, events.STAFF_REPLY, {"conversation_id": conversation.id})
        
    db.commit()
    db.refresh(msg)
    return msg
