from mongoengine import Document, EmbeddedDocument, fields, ReferenceField
from datetime import datetime
from bson import ObjectId

class Message(EmbeddedDocument):
    id = fields.ObjectIdField(default=lambda: ObjectId())
    role = fields.StringField(required=True, choices=['user', 'assistant'])
    content = fields.StringField(required=True)
    timestamp = fields.DateTimeField(default=datetime.utcnow)

class ChatSession(Document):
    user = ReferenceField('User', required=True)
    title = fields.StringField(default="New Chat")
    messages = fields.EmbeddedDocumentListField(Message, default=list)
    context = fields.DictField(default=dict) # Add context field
    created_at = fields.DateTimeField(default=datetime.utcnow)
    updated_at = fields.DateTimeField(default=datetime.utcnow)
    is_active = fields.BooleanField(default=True) # Add is_active field
    
    meta = {
        'collection': 'chat_sessions',
        'indexes': [
            'user',
            ('user', '-created_at'),
        ]
    }

    def save(self, *args, **kwargs):
        if not self.title and self.messages:
            # Generate title from first message if not set
            first_msg = self.messages.content
            self.title = first_msg[:50] + "..." if len(first_msg) > 50 else first_msg
        
        self.updated_at = datetime.utcnow()
        return super(ChatSession, self).save(*args, **kwargs)