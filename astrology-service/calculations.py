from datetime import datetime
from typing import Dict, Any
from jhora.horoscope.chart import charts
from skyfield.api import load, Topos
from pytz import timezone as pytz_timezone
 
def calculate_birth_chart(
    birth_date: str,
    birth_time: str,
    latitude: float,
    longitude: float,
    timezone: str
) -> Dict[str, Any]:
    """Calculate complete birth chart data using Skyfield and PyJHora."""
    try:
        # Set up Skyfield
        ts = load.timescale()
        eph = load('de421.bsp')
        
        # Parse birth datetime and localize it
        tz = pytz_timezone(timezone)
        birth_dt_naive = datetime.strptime(f"{birth_date} {birth_time}", "%Y-%m-%d %H:%M")
        birth_dt_aware = tz.localize(birth_dt_naive)
        
        # Create Skyfield time object
        t = ts.from_datetime(birth_dt_aware)
        
        # Set observer location
        observer = Topos(latitude_degrees=latitude, longitude_degrees=longitude)
        
        # Define planets
        planets = {
            'sun': eph['sun'],
            'moon': eph['moon'],
            'mercury': eph['mercury'],
            'venus': eph['venus'],
            'mars': eph['mars'],
            'jupiter': eph['jupiter barycenter'],
            'saturn': eph['saturn barycenter'],
            'uranus': eph['uranus barycenter'],
            'neptune': eph['neptune barycenter'],
            'pluto': eph['pluto barycenter']
        }
        
        # Calculate geocentric positions
        planet_positions = {}
        for name, body in planets.items():
            astrometric = (eph['earth'] + observer).at(t).observe(body)
            ra, dec, distance = astrometric.radec()
            planet_positions[name] = {
                'ra': ra.hours,
                'dec': dec.degrees,
                'distance': distance.au
            }
            
    except ValueError:
        raise ValueError("Invalid date or time format. Use YYYY-MM-DD and HH:MM.")
    
    # Calculate houses using Sripathi system with PyJHora
    # Note: PyJHora integration requires passing planet positions
    # This part needs to be adapted based on how PyJHora accepts planetary data
    houses = {} # Placeholder for PyJHora integration
    
    # Placeholder for aspects
    aspects = []
 
    return {
        'planet_positions': planet_positions,
        'houses': houses,
        'aspects': aspects,
        'birth_data': {
            'date': birth_date,
            'time': birth_time,
            'latitude': latitude,
            'longitude': longitude,
            'timezone': timezone
        }
    }
