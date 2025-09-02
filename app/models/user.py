from datetime import datetime
from mongoengine import Document, StringField, DateTimeField, DictField, BooleanField, ObjectIdField

class User(Document):
    email = StringField(required=True, unique=True)
    password_hash = StringField(required=False)
    name = StringField()
    authProvider = StringField()
    googleId = StringField()
    avatarUrl = StringField()
    chartId = ObjectIdField()
    preferences = DictField(default={})  # User preferences for content generation
    refresh_token = StringField()
    is_active = BooleanField(default=True)
    last_login = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'users',
        'indexes': [
            'email',
            'refresh_token',
            ('email', 'is_active'),
        ]
    }

    def update_last_login(self):
        """Update the last login timestamp."""
        self.last_login = datetime.utcnow()
        self.save()
