from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from calculations import calculate_birth_chart

app = FastAPI(title="Astrology Calculation Service")

class BirthData(BaseModel):
    birth_date: str  # Format: YYYY-MM-DD
    birth_time: str  # Format: HH:MM
    latitude: float
    longitude: float
    timezone: str

@app.post("/calculate-chart")
async def calculate_chart(birth_data: BirthData):
    try:
        chart_data = calculate_birth_chart(
            birth_date=birth_data.birth_date,
            birth_time=birth_data.birth_time,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone
        )
        return chart_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
