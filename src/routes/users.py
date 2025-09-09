"""User routes for the FastAPI application."""
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database.db import get_session
from ..models import User

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    """User creation schema."""

    name: str
    username: str
    password: str


class UserResponse(BaseModel):
    """User response schema."""

    id: int
    name: str
    username: str
    created_at: datetime
    updated_at: datetime | None

    class Config:
        """User response config."""

        from_attributes = True


@router.get("/", response_model=List[UserResponse])
async def get_users(session: Session = Depends(get_session)):
    """Get all users."""
    statement = select(User)

    result = session.execute(statement)
    users = result.scalars().all()

    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    """Get a specific user by ID."""
    pass


@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate, session: Session = Depends(get_session)
):
    """Create a new user."""
    pass


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserCreate,
    session: Session = Depends(get_session),
):
    """Update an existing user."""
    pass


@router.delete("/{user_id}")
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    """Delete a user."""
    pass
