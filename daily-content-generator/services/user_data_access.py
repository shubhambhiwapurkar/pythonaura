from datetime import datetime
from mongoengine import connect, Document, ReferenceField, DictField, DateTimeField, BooleanField, StringField
from ..config import settings

# Connect to MongoDB
connect(host=settings.get('MONGO_URI'))

class User(Document):
    """User model for accessing user data."""
    email = StringField(required=True, unique=True)
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    birth_details = DictField(required=True)
    preferences = DictField(default={})
    is_active = BooleanField(default=True)

    meta = {'collection': 'users'}

class DailyContent(Document):
    """Daily content model."""
    user = ReferenceField('User', required=True)
    date = DateTimeField(required=True)
    content = DictField(required=True)
    type = StringField(required=True)
    read_status = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'daily_content'}

def get_active_users():
    """Get all active users from the database."""
    return User.objects(is_active=True)

def get_user_by_id(user_id):
    """Get a single user by their ID."""
    try:
        return User.objects(id=user_id).first()
    except Exception:
        return None

def create_daily_content(user_id, content):
    """Create a new daily content entry for a user."""
    daily_content = DailyContent(
        user=user_id,
        date=datetime.utcnow(),
        content=content,
        type='daily_horoscope'
    )
    daily_content.save()
    return daily_content
