"""
Todo management API endpoints.
"""

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json, JSONResponse
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from .database import get_db

# Create blueprint
todos_bp = Blueprint("todos")

# Pydantic models for request validation
class TodoCreate(BaseModel):
    title: str
    description: str
    user_id: int
    completed: Optional[bool] = False

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    user_id: Optional[int] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    user_id: int
    created_at: str

@todos_bp.get("/todos")
async def get_todos(request: Request) -> JSONResponse:
    """Get all todos."""
    try:
        db = get_db()
        todos = db.find_all('todos')
        
        # Optional filtering by user_id
        user_id = request.args.get('user_id')
        if user_id:
            try:
                user_id = int(user_id)
                todos = [todo for todo in todos if todo['user_id'] == user_id]
            except ValueError:
                return json({"error": "Invalid user_id parameter"}, status=400)
        
        # Optional filtering by completion status
        completed = request.args.get('completed')
        if completed is not None:
            completed_bool = completed.lower() in ['true', '1', 'yes']
            todos = [todo for todo in todos if todo['completed'] == completed_bool]
        
        return json(todos)
    except Exception as e:
        return json({"error": str(e)}, status=500)

@todos_bp.get("/todos/<todo_id:int>")
async def get_todo(request: Request, todo_id: int) -> JSONResponse:
    """Get a specific todo by ID."""
    try:
        db = get_db()
        todo = db.find_by_id('todos', todo_id)
        
        if not todo:
            return json({"error": "Todo not found"}, status=404)
        
        return json(todo)
    except Exception as e:
        return json({"error": str(e)}, status=500)

@todos_bp.post("/todos")
async def create_todo(request: Request) -> JSONResponse:
    """Create a new todo."""
    try:
        # Validate request data
        try:
            todo_data = TodoCreate(**request.json)
        except ValidationError as e:
            return json({"error": "Validation error", "details": e.errors()}, status=400)
        
        db = get_db()
        
        # Check if user exists
        user = db.find_by_id('users', todo_data.user_id)
        if not user:
            return json({"error": "User not found"}, status=400)
        
        # Create todo
        new_todo = db.insert('todos', todo_data.model_dump())
        
        return json(new_todo, status=201)
    except Exception as e:
        return json({"error": str(e)}, status=500)

@todos_bp.put("/todos/<todo_id:int>")
async def update_todo(request: Request, todo_id: int) -> JSONResponse:
    """Update a todo."""
    try:
        # Validate request data
        try:
            todo_data = TodoUpdate(**request.json)
        except ValidationError as e:
            return json({"error": "Validation error", "details": e.errors()}, status=400)
        
        db = get_db()
        
        # Check if todo exists
        existing_todo = db.find_by_id('todos', todo_id)
        if not existing_todo:
            return json({"error": "Todo not found"}, status=404)
        
        # Check if user exists (if user_id is being updated)
        if todo_data.user_id:
            user = db.find_by_id('users', todo_data.user_id)
            if not user:
                return json({"error": "User not found"}, status=400)
        
        # Update todo
        updates = {k: v for k, v in todo_data.model_dump().items() if v is not None}
        updated_todo = db.update_by_id('todos', todo_id, updates)
        
        return json(updated_todo)
    except Exception as e:
        return json({"error": str(e)}, status=500)

@todos_bp.delete("/todos/<todo_id:int>")
async def delete_todo(request: Request, todo_id: int) -> JSONResponse:
    """Delete a todo."""
    try:
        db = get_db()
        
        # Check if todo exists
        existing_todo = db.find_by_id('todos', todo_id)
        if not existing_todo:
            return json({"error": "Todo not found"}, status=404)
        
        # Delete todo
        success = db.delete_by_id('todos', todo_id)
        
        if success:
            return json({"message": "Todo deleted successfully"})
        else:
            return json({"error": "Failed to delete todo"}, status=500)
    except Exception as e:
        return json({"error": str(e)}, status=500)

@todos_bp.get("/users/<user_id:int>/todos")
async def get_user_todos(request: Request, user_id: int) -> JSONResponse:
    """Get all todos for a specific user."""
    try:
        db = get_db()
        
        # Check if user exists
        user = db.find_by_id('users', user_id)
        if not user:
            return json({"error": "User not found"}, status=404)
        
        # Get user's todos
        todos = db.find_by_field('todos', 'user_id', user_id)
        
        return json(todos)
    except Exception as e:
        return json({"error": str(e)}, status=500)
