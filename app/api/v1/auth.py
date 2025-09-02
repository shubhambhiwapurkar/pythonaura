from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
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
        birth_details=user_data.birth_details
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
