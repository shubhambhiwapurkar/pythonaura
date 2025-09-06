from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.models.dailycontent import DailyContent
from app.models.user import User
from app.services.daily_content_service import DailyContentService
from datetime import datetime
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class Transit(BaseModel):
    transit: str
    description: str

class DailyContentResponse(BaseModel):
    dailyAffirmation: str
    keyTransits: list[Transit]
    dailyChartInsight: str
    exploreTopic: str

@router.get("/", response_model=DailyContentResponse)
async def get_daily_content(current_user: User = Depends(get_current_user)):
    """Get daily content for the current user."""
    content = await DailyContentService.get_or_generate_daily_content(current_user)
    return content
