"""
User management API endpoints.
"""

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, JSONResponse
from pydantic import BaseModel, ValidationError, field_validator
from typing import List, Optional
import re
from .database import get_db

# Create blueprint
users_bp = Blueprint("users")

# Pydantic models for request validation
class UserCreate(BaseModel):
    name: str
    email: str
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is not None:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, v):
                raise ValueError('Invalid email format')
        return v

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: str

@users_bp.get("/users")
async def get_users(request: Request) -> JSONResponse:
    """Get all users."""
    try:
        db = get_db()
        users = db.find_all('users')
        return json(users)
    except Exception as e:
        return json({"error": str(e)}, status=500)

@users_bp.get("/users/<user_id:int>")
async def get_user(request: Request, user_id: int) -> JSONResponse:
    """Get a specific user by ID."""
    try:
        db = get_db()
        user = db.find_by_id('users', user_id)
        
        if not user:
            return json({"error": "User not found"}, status=404)
        
        return json(user)
    except Exception as e:
        return json({"error": str(e)}, status=500)

@users_bp.post("/users")
async def create_user(request: Request) -> JSONResponse:
    """Create a new user."""
    try:
        # Validate request data
        try:
            user_data = UserCreate(**request.json)
        except ValidationError as e:
            return json({"error": "Validation error", "details": e.errors()}, status=400)
        
        db = get_db()
        
        # Check if email already exists
        existing_users = db.find_by_field('users', 'email', user_data.email)
        if existing_users:
            return json({"error": "Email already exists"}, status=400)
        
        # Create user
        new_user = db.insert('users', user_data.model_dump())
        
        return json(new_user, status=201)
    except Exception as e:
        return json({"error": str(e)}, status=500)

@users_bp.put("/users/<user_id:int>")
async def update_user(request: Request, user_id: int) -> JSONResponse:
    """Update a user."""
    try:
        # Validate request data
        try:
            user_data = UserUpdate(**request.json)
        except ValidationError as e:
            return json({"error": "Validation error", "details": e.errors()}, status=400)
        
        db = get_db()
        
        # Check if user exists
        existing_user = db.find_by_id('users', user_id)
        if not existing_user:
            return json({"error": "User not found"}, status=404)
        
        # Check if email already exists (if email is being updated)
        if user_data.email:
            existing_email_users = db.find_by_field('users', 'email', user_data.email)
            if existing_email_users and existing_email_users[0]['id'] != user_id:
                return json({"error": "Email already exists"}, status=400)
        
        # Update user
        updates = {k: v for k, v in user_data.model_dump().items() if v is not None}
        updated_user = db.update_by_id('users', user_id, updates)
        
        return json(updated_user)
    except Exception as e:
        return json({"error": str(e)}, status=500)

@users_bp.delete("/users/<user_id:int>")
async def delete_user(request: Request, user_id: int) -> JSONResponse:
    """Delete a user."""
    try:
        db = get_db()
        
        # Check if user exists
        existing_user = db.find_by_id('users', user_id)
        if not existing_user:
            return json({"error": "User not found"}, status=404)
        
        # Delete user
        success = db.delete_by_id('users', user_id)
        
        if success:
            return json({"message": "User deleted successfully"})
        else:
            return json({"error": "Failed to delete user"}, status=500)
    except Exception as e:
        return json({"error": str(e)}, status=500)
