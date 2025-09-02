from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User
from app.models.birthchart import BirthChart
from app.services.astrology_client import create_birth_chart, get_daily_transits
from app.core.dependencies import get_current_user
from pydantic import BaseModel

router = APIRouter()

class BirthData(BaseModel):
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str

@router.post("/")
async def create_chart(birth_data: BirthData, current_user: User = Depends(get_current_user)):
    """Create a new birth chart for the current user."""
    chart_data = await create_birth_chart(birth_data.dict())
    if not chart_data:
        raise HTTPException(status_code=500, detail="Failed to create birth chart")
    
    birth_chart = BirthChart(
        user_id=current_user.id,
        birth_details=birth_data.dict(),
        chart_data=chart_data
    )
    birth_chart.save()
    
    return birth_chart

@router.get("/{chart_id}")
async def get_chart(chart_id: str, current_user: User = Depends(get_current_user)):
    """Retrieve a specific birth chart for the current user."""
    birth_chart = BirthChart.objects(id=chart_id, user_id=current_user.id).first()
    if not birth_chart:
        raise HTTPException(status_code=404, detail="Birth chart not found")
    return birth_chart

@router.get("/user")
async def get_user_charts(current_user: User = Depends(get_current_user)):
    """Retrieve all birth charts for the current user."""
    birth_charts = BirthChart.objects(user_id=current_user.id)
    return list(birth_charts)

@router.get("/{chart_id}/transits")
async def get_transits(chart_id: str, current_user: User = Depends(get_current_user)):
    """Retrieve daily transits for a specific birth chart."""
    birth_chart = BirthChart.objects(id=chart_id, user_id=current_user.id).first()
    if not birth_chart:
        raise HTTPException(status_code=404, detail="Birth chart not found")
    
    transits_data = await get_daily_transits(chart_id)
    if not transits_data:
        raise HTTPException(status_code=500, detail="Failed to get daily transits")
        
    return transits_data