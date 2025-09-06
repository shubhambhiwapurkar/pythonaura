from fastapi import APIRouter, Depends
from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter()

from fastapi import HTTPException, status
from app.models.chat import ChatSession

@router.delete("/account")
async def delete_account(current_user: User = Depends(get_current_user)):
    """Delete the current user's account and all associated data."""
    try:
        user_id = str(current_user.id)  # Convert ObjectId to string
        
        # Delete all chat sessions associated with the user
        ChatSession.objects(user=user_id).delete()
        
        # Delete all birth charts associated with the user
        from app.models.birthchart import BirthChart
        BirthChart.objects(user=user_id).delete()
        
        # Delete the user account
        current_user.delete()
        
        return {
            "message": "Account successfully deleted",
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete account: {str(e)}"
        )