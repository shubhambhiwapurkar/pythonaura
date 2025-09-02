from datetime import datetime
from mongoengine import connect, disconnect
from models.user import User
from models.birthchart import BirthChart
from core.security import get_password_hash
from core.config import get_settings

def init_test_data():
    """Initialize test data in the database."""
    # Ensure we're disconnected before connecting
    disconnect()
    
    # Connect to MongoDB
    settings = get_settings()
    connect(host=settings.MONGODB_URI)
    
    # Create a test user
    test_user = User(
        email="test@example.com",
        password_hash=get_password_hash("testpassword123"),
        first_name="Test",
        last_name="User",
        birth_details={
            "date": "1990-01-01",
            "time": "12:00",
            "location": "New York, USA",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timezone": "America/New_York"
        },
        preferences={
            "focus_areas": ["Career", "Relationships", "Personal Growth"]
        },
        is_active=True,
        created_at=datetime.utcnow()
    )
    test_user.save()
    
    # Create a test birth chart
    test_chart = BirthChart(
        user=test_user,
        birth_details=test_user.birth_details,
        chart_data={
            "planets": {
                "sun": {"sign": "Capricorn", "degree": 10.5},
                "moon": {"sign": "Aries", "degree": 15.3},
                # Add more planet positions
            },
            "houses": {
                "1": 0.0,
                "2": 30.0,
                "3": 60.0,
                # Add more house cusps
            },
            "aspects": [
                {
                    "planet1": "sun",
                    "planet2": "moon",
                    "aspect": "square",
                    "orb": 4.8
                }
                # Add more aspects
            ]
        },
        created_at=datetime.utcnow()
    )
    test_chart.save()
    
    print("Test data initialized successfully!")

if __name__ == "__main__":
    init_test_data()
