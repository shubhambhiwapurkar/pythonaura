import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from bson import ObjectId
import google.generativeai as genai
from app.models.chat import ChatSession, Message
from app.models.user import User
from app.services.chat_service import ChatService

# Mock Google AI configuration
patch('google.generativeai.configure').start()
mock_model = Mock(genai.GenerativeModel)
patch('google.generativeai.GenerativeModel', return_value=mock_model).start()

@pytest.fixture
def mock_user():
    return Mock(User, id=ObjectId())

@pytest.fixture
def mock_chat_session(mock_user):
    session = Mock(ChatSession)
    session.id = ObjectId()
    session.user_id = mock_user.id
    session.title = "Test Chat"
    session.is_active = True
    session.messages = []
    session.context = {}
    session.created_at = datetime.utcnow()
    session.updated_at = datetime.utcnow()
    session.save = AsyncMock(return_value=session)
    return session

@pytest.mark.asyncio
async def test_create_session(mock_user):
    with patch('app.models.chat.ChatSession') as MockChatSession:
        # Setup
        mock_session = Mock()
        mock_session.save.return_value = mock_session
        MockChatSession.return_value = mock_session
        
        # Execute
        title = "Test Chat"
        context = {"test": "context"}
        result = await ChatService.create_session(mock_user, title, context)
        
        # Assert
        MockChatSession.assert_called_once_with(
            user_id=mock_user.id,
            title=title,
            context=context
        )
        mock_session.save.assert_called_once()
        assert result == mock_session

@pytest.mark.asyncio
async def test_get_user_sessions(mock_user):
    with patch('app.models.chat.ChatSession.objects') as mock_objects:
        # Setup
        mock_query = Mock()
        mock_objects.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = [Mock(ChatSession), Mock(ChatSession)]
        
        # Execute
        sessions = await ChatService.get_user_sessions(mock_user, active_only=True)
        
        # Assert
        mock_objects.assert_called_once_with(user_id=mock_user.id)
        mock_query.filter.assert_called_once_with(is_active=True)
        mock_query.order_by.assert_called_once_with('-updated_at')
        assert len(sessions) == 2

@pytest.mark.asyncio
async def test_get_session(mock_user, mock_chat_session):
    with patch('app.models.chat.ChatSession.objects') as mock_objects:
        # Setup
        mock_query = Mock()
        mock_objects.return_value = mock_query
        mock_query.first.return_value = mock_chat_session
        session_id = str(mock_chat_session.id)
        
        # Execute
        result = await ChatService.get_session(session_id, mock_user)
        
        # Assert
        mock_objects.assert_called_once_with(
            id=mock_chat_session.id,
            user_id=mock_user.id
        )
        assert result == mock_chat_session

@pytest.mark.asyncio
async def test_add_message(mock_chat_session):
    # Setup
    content = "Test message"
    message_type = "user"
    
    # Execute
    result = await ChatService.add_message(mock_chat_session, content, message_type)
    
    # Assert
    assert isinstance(result, Message)
    assert result.content == content
    assert result.message_type == message_type
    assert 'client_timestamp' in result.metadata
    mock_chat_session.messages.append.assert_called_once()
    mock_chat_session.save.assert_called_once()

@pytest.mark.asyncio
async def test_generate_response(mock_chat_session):
    with patch('google.generativeai.GenerativeModel.generate_content') as mock_generate:
        # Setup
        mock_response = Mock()
        mock_response.text = "AI response"
        mock_generate.return_value = mock_response
        mock_chat_session.messages = [
            Mock(Message, message_type='user', content='Hello'),
            Mock(Message, message_type='assistant', content='Hi there')
        ]
        user_message = "How are you?"
        
        # Execute
        result = await ChatService.generate_response(mock_chat_session, user_message)
        
        # Assert
        mock_generate.assert_called_once()
        assert result == "AI response"

@pytest.mark.asyncio
async def test_generate_response_with_context(mock_chat_session):
    with patch('google.generativeai.GenerativeModel.generate_content') as mock_generate:
        # Setup
        mock_response = Mock()
        mock_response.text = "Contextual AI response"
        mock_generate.return_value = mock_response
        mock_chat_session.context = {"user_preference": "technical"}
        user_message = "Explain this concept"
        
        # Execute
        result = await ChatService.generate_response(mock_chat_session, user_message)
        
        # Assert
        mock_generate.assert_called_once()
        call_args = mock_generate.call_args[0][0]
        assert any("Context Information" in msg['content'] for msg in call_args if msg['role'] == 'system')
        assert result == "Contextual AI response"

@pytest.mark.asyncio
async def test_generate_response_error_handling(mock_chat_session):
    with patch('google.generativeai.GenerativeModel.generate_content') as mock_generate:
        # Setup
        mock_generate.side_effect = Exception("API Error")
        user_message = "This will fail"
        
        # Execute
        result = await ChatService.generate_response(mock_chat_session, user_message)
        
        # Assert
        assert "I apologize" in result
        assert "try again" in result

@pytest.mark.asyncio
async def test_end_session(mock_chat_session):
    # Execute
    await ChatService.end_session(mock_chat_session)
    
    # Assert
    assert mock_chat_session.is_active is False
    mock_chat_session.save.assert_called_once()

@pytest.mark.asyncio
async def test_delete_session(mock_chat_session):
    # Setup
    mock_chat_session.delete = AsyncMock()
    
    # Execute
    await ChatService.delete_session(mock_chat_session)
    
    # Assert
    mock_chat_session.delete.assert_called_once()
