import os
from pathlib import Path
from dotenv import load_dotenv

# Load test environment variables
test_env_path = Path(__file__).parent / '.env.test'
load_dotenv(test_env_path)

def get_test_settings():
    """Get test settings from environment variables."""
    return {
        'MONGODB_URI': os.getenv('MONGODB_URI'),
        'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY'),
        'GOOGLE_MAPS_API_KEY': os.getenv('GOOGLE_MAPS_API_KEY'),
        'GOOGLE_AI_API_KEY': os.getenv('GOOGLE_AI_API_KEY'),
        'ASTROLOGY_SERVICE_URL': os.getenv('ASTROLOGY_SERVICE_URL')
    }
