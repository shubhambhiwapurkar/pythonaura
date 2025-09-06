from typing import List, Optional
from datetime import datetime
from app.models.chat import ChatSession, Message
from app.models.user import User
import google.generativeai as genai
from app.core.config import settings
from bson import ObjectId

# Configure the AI model
genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

class ChatService:
    @staticmethod
    async def create_session(user: User, title: str = None, context: dict = None) -> ChatSession:
        """Create a new chat session."""
        session = ChatSession(
            user=user,
            title=title or "New Chat",
            context=context or {}
        ).save()
        return session

    @staticmethod
    async def get_user_sessions(user: User, active_only: bool = True) -> List[ChatSession]:
        """Get all chat sessions for a user."""
        query = ChatSession.objects(user_id=user.id)
        if active_only:
            query = query.filter(is_active=True)
        return list(query.order_by('-updated_at'))

    @staticmethod
    async def get_session(session_id: str, user: User) -> Optional[ChatSession]:
        """Get a specific chat session."""
        try:
            return ChatSession.objects(id=ObjectId(session_id), user=user).first()
        except Exception:
            return None

    @staticmethod
    async def add_message(session: ChatSession, content: str, message_type: str) -> Message:
        """Add a message to a chat session."""
        message = Message(
            role=message_type,
            content=content
        )
        session.messages.append(message)
        session.save()
        return message

    @staticmethod
    async def generate_response(session: ChatSession, user_message: str) -> str:
        """Generate an AI response based on the chat context and user message."""
        # Prepare conversation history
        conversation_history = []
        for msg in session.messages[-5:]:  # Get last 5 messages for context
            conversation_history.append({
                'role': msg.message_type,
                'content': msg.content
            })
        
        # Add custom context if available
        context_prompt = ""
        if session.context:
            context_list = [f"{key}: {value}" for key, value in session.context.items()]
            context_prompt = "\nContext Information:\n" + "\n".join(context_list)
        
        # Prepare the prompt
        system_prompt = f"""You are an AI assistant trained to provide helpful and informative responses.
        Maintain a professional and supportive tone in your responses.{context_prompt}
        
        Keep responses clear, concise, and relevant to the user's query."""
        
        try:
            # Generate response using the AI model
            response = model.generate_content([
                {'role': 'system', 'content': system_prompt},
                *conversation_history,
                {'role': 'user', 'content': user_message}
            ])
            
            return response.text
            
        except Exception as e:
            # Log the error and return a fallback response
            print(f"Error generating AI response: {str(e)}")
            return "I apologize, but I'm having trouble generating a response right now. Please try again in a moment."

    @staticmethod
    async def end_session(session: ChatSession):
        """End a chat session."""
        session.is_active = False
        session.save()

    @staticmethod
    async def delete_session(session: ChatSession):
        """Delete a chat session and all its messages."""
        session.delete()
