"""
Mock database implementation with in-memory storage.
In production, this would be replaced with a real database like PostgreSQL or MongoDB.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import threading

class MockDatabase:
    """Thread-safe in-memory database for demonstration purposes."""
    
    def __init__(self):
        self._data: Dict[str, List[Dict[str, Any]]] = {
            'users': [],
            'todos': []
        }
        self._counters: Dict[str, int] = {
            'users': 0,
            'todos': 0
        }
        self._lock = threading.Lock()
    
    def _get_next_id(self, table: str) -> int:
        """Get the next ID for a table."""
        with self._lock:
            self._counters[table] += 1
            return self._counters[table]
    
    def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new record into the specified table."""
        with self._lock:
            record = {
                'id': self._get_next_id(table),
                **data,
                'created_at': datetime.utcnow().isoformat()
            }
            self._data[table].append(record)
            return record.copy()
    
    def find_all(self, table: str) -> List[Dict[str, Any]]:
        """Get all records from the specified table."""
        with self._lock:
            return [record.copy() for record in self._data[table]]
    
    def find_by_id(self, table: str, record_id: int) -> Optional[Dict[str, Any]]:
        """Find a record by ID."""
        with self._lock:
            for record in self._data[table]:
                if record['id'] == record_id:
                    return record.copy()
            return None
    
    def find_by_field(self, table: str, field: str, value: Any) -> List[Dict[str, Any]]:
        """Find records by a specific field value."""
        with self._lock:
            results = []
            for record in self._data[table]:
                if record.get(field) == value:
                    results.append(record.copy())
            return results
    
    def update_by_id(self, table: str, record_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record by ID."""
        with self._lock:
            for i, record in enumerate(self._data[table]):
                if record['id'] == record_id:
                    # Update the record
                    for key, value in updates.items():
                        if key != 'id':  # Don't allow ID updates
                            record[key] = value
                    record['updated_at'] = datetime.utcnow().isoformat()
                    return record.copy()
            return None
    
    def delete_by_id(self, table: str, record_id: int) -> bool:
        """Delete a record by ID."""
        with self._lock:
            for i, record in enumerate(self._data[table]):
                if record['id'] == record_id:
                    del self._data[table][i]
                    return True
            return False
    
    def clear_table(self, table: str) -> None:
        """Clear all records from a table."""
        with self._lock:
            self._data[table] = []
            self._counters[table] = 0

# Global database instance
db = MockDatabase()

def init_db():
    """Initialize the database with sample data."""
    # Clear existing data
    db.clear_table('users')
    db.clear_table('todos')
    
    # Add sample users
    sample_users = [
        {"name": "John Doe", "email": "john@example.com"},
        {"name": "Jane Smith", "email": "jane@example.com"},
        {"name": "Bob Johnson", "email": "bob@example.com"}
    ]
    
    for user_data in sample_users:
        db.insert('users', user_data)
    
    # Add sample todos
    sample_todos = [
        {
            "title": "Setup project structure",
            "description": "Create the initial project structure with Next.js and Sanic",
            "completed": True,
            "user_id": 1
        },
        {
            "title": "Implement user authentication",
            "description": "Add user login and registration functionality",
            "completed": False,
            "user_id": 1
        },
        {
            "title": "Design database schema",
            "description": "Plan the database structure for the application",
            "completed": False,
            "user_id": 2
        },
        {
            "title": "Write API documentation",
            "description": "Document all API endpoints and their usage",
            "completed": False,
            "user_id": 3
        }
    ]
    
    for todo_data in sample_todos:
        db.insert('todos', todo_data)

def get_db() -> MockDatabase:
    """Get the database instance."""
    return db
