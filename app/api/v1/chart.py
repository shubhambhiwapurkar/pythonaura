from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.models.user import User
from app.models.birthchart import BirthChart
from app.services.astrology_client import create_birth_chart, get_daily_transits
from app.core.dependencies import get_current_user
from bson import ObjectId
from pydantic import BaseModel
import httpx
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class BirthData(BaseModel):
    birth_date: str
    birth_time: str
    birth_place: str
    latitude: float
    longitude: float
    timezone: str

async def trigger_daily_content_generation(user_id: str):
    """Asynchronously triggers the Azure Function to generate daily content for a specific user."""
    function_url = os.getenv("daily-content-func-url")
    function_key = os.getenv("daily-content-func-key")

    if not function_url or not function_key:
        logger.error("Azure Function URL or Key not set in environment variables.")
        return

    headers = {"x-functions-key": function_key}
    params = {"user_id": user_id}
    
    try:
        async with httpx.AsyncClient() as client:
            logger.info(f"Triggering daily content generation for user_id: {user_id}")
            response = await client.post(function_url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            logger.info(f"Successfully triggered daily content generation for user_id: {user_id}. Status: {response.status_code}")
    except httpx.RequestError as e:
        logger.error(f"Error calling Azure Function for user_id {user_id}: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while triggering Azure function for user_id {user_id}: {e}")


@router.post("/")
async def create_chart(
    birth_data: BirthData, 
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Create a new birth chart for the current user and trigger daily content generation."""
    # Check if a chart already exists
    if BirthChart.objects(user=str(current_user.id)).first():
        raise HTTPException(status_code=409, detail="A birth chart for this user already exists.")

    chart_data = await create_birth_chart(birth_data.dict())
    if not chart_data:
        raise HTTPException(status_code=500, detail="Failed to create birth chart from astrology service")
    
    birth_chart = BirthChart(
        user=str(current_user.id),
        birth_data=birth_data.dict(),
        chart_data=chart_data
    )
    birth_chart.save()

    # Add a background task to trigger the Azure function
    user_id_str = str(current_user.id)
    background_tasks.add_task(trigger_daily_content_generation, user_id_str)
    
    # Update user model with birth details
    current_user.birth_details = {
        "date": birth_data.birth_date,
        "time": birth_data.birth_time,
        "place": birth_data.birth_place,
    }
    current_user.save()

    return birth_chart

@router.get("/{chart_id}")
async def get_chart(chart_id: str, current_user: User = Depends(get_current_user)):
    """Retrieve a specific birth chart for the current user."""
    try:
        user_id = str(current_user.id)  # Get string representation of ObjectId
        birth_chart = BirthChart.objects(id=chart_id, user=user_id).first()
        if not birth_chart:
            raise HTTPException(status_code=404, detail="Birth chart not found")
        return birth_chart
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving birth chart: {str(e)}")

@router.get("/user")
async def get_user_charts(current_user: User = Depends(get_current_user)):
    """Retrieve all birth charts for the current user."""
    try:
        birth_charts = BirthChart.objects(user=current_user.id)
        return list(birth_charts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving birth charts: {str(e)}")

@router.get("/{chart_id}/transits")
async def get_transits(chart_id: str, current_user: User = Depends(get_current_user)):
    """Retrieve daily transits for a specific birth chart."""
    birth_chart = BirthChart.objects(id=ObjectId(chart_id), user=ObjectId(str(current_user.id))).first()
    if not birth_chart:
        raise HTTPException(status_code=404, detail="Birth chart not found")
    
    transits_data = await get_daily_transits(chart_id)
    if not transits_data:
        raise HTTPException(status_code=500, detail="Failed to get daily transits")
        
    return transits_data