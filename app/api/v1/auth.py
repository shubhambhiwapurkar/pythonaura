from datetime import timedelta
import httpx
from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token
)
from app.core.config import get_settings
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.core.dependencies import get_current_user

settings = get_settings()

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    birth_details: dict

class Token(BaseModel):
    access_token: str
    refresh_token: str
class TokenData(BaseModel):
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    first_name: str
    last_name: str
    birth_details: dict

    token_type: str

@router.post("/signup", response_model=Token)
async def signup(user_data: UserCreate):
    """Create a new user account."""
    if User.objects(email=user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        birth_details=user_data.birth_details,
        name=f"{user_data.first_name} {user_data.last_name}" # Combine for existing 'name' field
    )
    user.save()

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    user.refresh_token = refresh_token
    user.save()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with email and password."""
    user = User.objects(email=form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user.update_last_login()
    
    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    user.refresh_token = refresh_token
    user.save()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

class RefreshToken(BaseModel):
    refresh_token: str

@router.post("/refresh-token", response_model=Token)
async def refresh_token(token_data: RefreshToken):
    """Get a new access token using a refresh token."""
    user = User.objects(refresh_token=token_data.refresh_token).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(str(user.id))
    refresh_token = create_refresh_token(str(user.id))
    user.refresh_token = refresh_token
    user.save()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout the current user."""
    current_user.refresh_token = None
    current_user.save()
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Fetch the current logged in user."""
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "birth_details": current_user.birth_details
    }

@router.get("/google")
async def google_login():
    """Redirect to Google for authentication."""
    return {
        "url": f"https://accounts.google.com/o/oauth2/v2/auth?"
               f"client_id={settings.GOOGLE_CLIENT_ID}&"
               f"redirect_uri={settings.GOOGLE_REDIRECT_URI}&"
               f"response_type=code&"
               f"scope=openid%20email%20profile"
    }

@router.get("/google/callback")
async def google_callback(request: Request):
    """Handle Google callback."""
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing authorization code"
        )

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_response.json()
        id_token = token_data.get("id_token")

        if not id_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing id_token"
            )

        user_info_response = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        user_info = user_info_response.json()
        email = user_info.get("email")
        google_id = user_info.get("sub")
        name = user_info.get("name")

        user = User.objects(email=email).first()
        if not user:
            user = User(
                email=email,
                googleId=google_id,
                name=name,
                authProvider="google",
            )
            user.save()

        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))
        user.refresh_token = refresh_token
        user.save()

        # Redirect to the frontend with the tokens
        return RedirectResponse(
            url=f"{settings.FRONTEND_CORS_ORIGINS[0]}/profile?access_token={access_token}&refresh_token={refresh_token}"
        )
