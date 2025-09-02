from mongoengine import connect, disconnect
from app.core.config import settings

def connect_to_mongodb():
    """Connect to MongoDB using the configured URI."""
    disconnect()  # Ensure any existing connections are closed
    connect(host=settings.MONGODB_URI)

def close_mongodb_connection():
    """Close the MongoDB connection."""
    disconnect()
