from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Chat, Message
import time

router = APIRouter(prefix="/chat", tags=["Chat"])

# Create new chat
@router.post("/create")
def create_chat(db: Session = Depends(get_db)):
    chat = Chat()
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

# List all chats
@router.get("/list")
def list_chats(db: Session = Depends(get_db)):
    return db.query(Chat).order_by(Chat.created_at.desc()).all()

# Get messages in a chat
@router.get("/{chat_id}/history")
def chat_history(chat_id: int, db: Session = Depends(get_db)):
    msgs = db.query(Message).filter(Message.chat_id == chat_id).all()
    return msgs

# Save new message + AI response
@router.post("/{chat_id}/send")
def send_message(chat_id: int, user_msg: str, db: Session = Depends(get_db)):
    # Save user message
    msg = Message(chat_id=chat_id, role="user", content=user_msg)
    db.add(msg)

    # --- your AI call here (example placeholder) ---
    # ai_response = ask_ai(user_msg) # we add streaming in step 3
    ai_response = f"Echo: {user_msg}"  # temporary
    # ------------------------------------------------

    # Save AI response
    ai_msg = Message(chat_id=chat_id, role="assistant", content=ai_response)
    db.add(ai_msg)

    db.commit()
    db.refresh(ai_msg)
    return ai_msg
