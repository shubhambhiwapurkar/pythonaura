from mongoengine import Document, EmbeddedDocument, fields, ReferenceField
from datetime import datetime
from bson import ObjectId

class Message(EmbeddedDocument):
    id = fields.ObjectIdField(default=lambda: ObjectId())
    role = fields.StringField(required=True, choices=['user', 'assistant'])
    content = fields.StringField(required=True)
    message_type = fields.StringField(default='text')  # Added for message type validation
    timestamp = fields.DateTimeField(default=datetime.utcnow)
    metadata = fields.DictField(default=dict)  # For storing any additional message metadata

class ChatSession(Document):
    user = fields.ObjectIdField(required=True)
    title = fields.StringField(default="New Chat")
    messages = fields.EmbeddedDocumentListField(Message, default=list)
    context = fields.DictField(default=dict)
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    is_active = fields.BooleanField(default=True)
    
    meta = {
        'collection': 'chat_sessions',
        'indexes': [
            'user',
            ('user', '-created_at'),
            '-updated_at',  # Add index for sorting by updated_at
            ('user', '-updated_at')  # Compound index for user's recent chats
        ]
    }

    def save(self, *args, **kwargs):
        if not self.title and self.messages:
            # Generate title from first user message if not set
            first_user_msg = next((msg for msg in self.messages if msg.role == 'user'), None)
            if first_user_msg:
                content = first_user_msg.content
                self.title = content[:50] + "..." if len(content) > 50 else content
        
        self.updated_at = datetime.utcnow()
        return super(ChatSession, self).save(*args, **kwargs)