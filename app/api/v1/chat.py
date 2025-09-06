from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.user import User
from app.models.chat import ChatSession, Message
from app.core.dependencies import get_current_user
from app.services.chat_service import ChatService

router = APIRouter()

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: str
    content: str
    role: str
    message_type: str
    created_at: datetime
    metadata: dict = {}

    class Config:
        from_attributes = True
        
    @classmethod
    def from_db_message(cls, message: Message):
        return cls(
            id=str(message.id),
            content=message.content,
            role=message.role,
            message_type=message.message_type,
            created_at=message.timestamp,
            metadata=message.metadata
        )

class SessionCreate(BaseModel):
    title: Optional[str] = None
    context: Optional[dict] = None

class SessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    message_count: int

    class Config:
        from_attributes = True

@router.post("/sessions", response_model=SessionResponse)
async def create_chat_session(
    session_data: SessionCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new chat session."""
    session = await ChatService.create_session(
        user=current_user,
        title=session_data.title,
        context=session_data.context
    )
    return {
        "id": str(session.id),
        "title": session.title,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "is_active": session.is_active,
        "message_count": len(session.messages)
    }

@router.get("/sessions", response_model=List[SessionResponse])
async def list_chat_sessions(
    active_only: bool = True,
    current_user: User = Depends(get_current_user)
):
    """List all chat sessions for the current user."""
    sessions = await ChatService.get_user_sessions(current_user, active_only)
    return [{
        "id": str(session.id),
        "title": session.title,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "is_active": session.is_active,
        "message_count": len(session.messages)
    } for session in sessions]

@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
async def send_message(
    session_id: str,
    message: MessageCreate,
    current_user: User = Depends(get_current_user)
):
    """Send a message in a chat session and get AI response."""
    # Get the session
    session = await ChatService.get_session(session_id, current_user)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    if not session.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chat session is no longer active"
        )
    
    # Add user's message
    user_message = await ChatService.add_message(
        session=session,
        content=message.content,
        message_type='user'
    )
    
    # Generate and add AI response
    ai_response = await ChatService.generate_response(session, message.content)
    ai_message = await ChatService.add_message(
        session=session,
        content=ai_response,
        message_type='assistant'
    )
    
    # Return the AI's response using the response model
    return MessageResponse.from_db_message(ai_message)

@router.get("/sessions/{session_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get all messages in a chat session."""
    session = await ChatService.get_session(session_id, current_user)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    return [MessageResponse.from_db_message(message) for message in session.messages]

@router.post("/sessions/{session_id}/end")
async def end_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """End a chat session."""
    session = await ChatService.get_session(session_id, current_user)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    await ChatService.end_session(session)
    return {"message": "Chat session ended successfully"}

@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a chat session and all its messages."""
    session = await ChatService.get_session(session_id, current_user)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    
    await ChatService.delete_session(session)
    return {"message": "Chat session deleted successfully"}

@router.get("/", response_model=List[MessageResponse])
async def get_chat_history(current_user: User = Depends(get_current_user)):
    """Get all messages for the current user."""
    # Get the most recent active session
    session = await ChatService.get_or_create_session(current_user)
    if not session:
        return []
    
    return [MessageResponse.from_db_message(message) for message in session.messages]