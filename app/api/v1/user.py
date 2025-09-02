from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter()

@router.delete("/account")
async def delete_account(current_user: User = Depends(get_current_user)):
    """Delete the current user's account."""
    current_user.delete()
    return {"message": "Account successfully deleted"}