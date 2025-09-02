from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from timezonefinder import TimezoneFinder
from app.core.config import get_settings

settings = get_settings()

geolocator = Nominatim(user_agent="astrology_app")
tf = TimezoneFinder()

async def get_coordinates(location_string: str) -> dict:
    """Resolve a location string to latitude, longitude, and timezone."""
    try:
        location = geolocator.geocode(location_string, timeout=10)
        if location:
            timezone = tf.timezone_at(lng=location.longitude, lat=location.latitude)
            return {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "address": location.address,
                "timezone": timezone
            }
        raise ValueError(f"Location not found: {location_string}")
    except (GeocoderTimedOut, GeocoderUnavailable) as e:
        raise ValueError(f"Geocoding service error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error geocoding location: {str(e)}")