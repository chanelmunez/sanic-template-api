"""
Vercel serverless function handler.
This file handles all API requests for the Vercel deployment.
"""

from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse, parse_qs

# Simple in-memory database for the serverless function
_db = {
    'users': [
        {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'created_at': '2024-01-01T00:00:00'},
        {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'created_at': '2024-01-02T00:00:00'},
        {'id': 3, 'name': 'Bob Johnson', 'email': 'bob@example.com', 'created_at': '2024-01-03T00:00:00'}
    ],
    'todos': [
        {'id': 1, 'title': 'Setup project', 'description': 'Create initial project structure', 'completed': True, 'user_id': 1, 'created_at': '2024-01-01T00:00:00'},
        {'id': 2, 'title': 'Implement auth', 'description': 'Add user authentication', 'completed': False, 'user_id': 1, 'created_at': '2024-01-01T01:00:00'},
        {'id': 3, 'title': 'Design database', 'description': 'Plan database structure', 'completed': False, 'user_id': 2, 'created_at': '2024-01-01T02:00:00'},
        {'id': 4, 'title': 'Write docs', 'description': 'Document API endpoints', 'completed': False, 'user_id': 3, 'created_at': '2024-01-01T03:00:00'}
    ]
}
_counters = {'users': 3, 'todos': 4}

def get_next_id(table):
    _counters[table] += 1
    return _counters[table]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle_request()
    
    def do_POST(self):
        self._handle_request()
    
    def do_PUT(self):
        self._handle_request()
    
    def do_DELETE(self):
        self._handle_request()
    
    def do_OPTIONS(self):
        self._send_cors_response()
    
    def _send_cors_response(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
    
    def _handle_request(self):
        try:
            # Parse the URL and extract path
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            query_params = parse_qs(parsed_url.query)
            
            # Debug info for troubleshooting
            debug_info = {
                "path": path,
                "query_params": query_params,
                "method": self.command,
                "headers": dict(self.headers)
            }
            
            # Route to appropriate handler
            if path == '/api/index.py' or path == '/api/':
                # This is the serverless function entry point
                # Check for query parameters that indicate the actual endpoint
                if 'path' in query_params:
                    actual_path = query_params['path'][0]
                else:
                    actual_path = path
                
                if 'health' in actual_path:
                    self._send_json_response({
                        "status": "healthy",
                        "message": "Python Sanic API is running",
                        "version": "1.0.0",
                        "debug": debug_info
                    })
                elif 'users' in actual_path:
                    self._handle_users_endpoint(actual_path)
                elif 'todos' in actual_path:
                    self._handle_todos_endpoint(actual_path)
                else:
                    self._send_json_response({
                        "message": "Welcome to Sanic + Next.js Template API",
                        "endpoints": {
                            "health": "/api/python/health",
                            "users": "/api/python/users",
                            "todos": "/api/python/todos"
                        },
                        "debug": debug_info
                    })
            elif path == '/api/health' or path == '/api/python/health':
                self._send_json_response({
                    "status": "healthy", 
                    "message": "Python Sanic API is running",
                    "version": "1.0.0"
                })
            elif '/users' in path:
                self._handle_users_endpoint(path)
            elif '/todos' in path:
                self._handle_todos_endpoint(path)
            else:
                self._send_json_response({
                    "error": f"Not Found: {path}",
                    "debug": debug_info
                }, 404)
                
        except Exception as e:
            import traceback
            self._send_json_response({
                "error": str(e),
                "traceback": traceback.format_exc()
            }, 500)
    
    def _handle_users_endpoint(self, path):
        try:
            if self.command == 'GET':
                if path.endswith('/users') or path.endswith('/users/') or 'users' in path and not any(char.isdigit() for char in path.split('users')[-1]):
                    self._send_json_response(_db['users'])
                else:
                    # Extract user ID from path
                    parts = path.split('/')
                    user_id_part = None
                    for i, part in enumerate(parts):
                        if part == 'users' and i + 1 < len(parts):
                            user_id_part = parts[i + 1]
                            break
                    
                    if user_id_part:
                        try:
                            user_id = int(user_id_part)
                            user = next((u for u in _db['users'] if u['id'] == user_id), None)
                            if user:
                                self._send_json_response(user)
                            else:
                                self._send_json_response({"error": "User not found"}, 404)
                        except ValueError:
                            self._send_json_response({"error": "Invalid user ID"}, 400)
                    else:
                        self._send_json_response({"error": "Invalid path"}, 400)
            
            elif self.command == 'POST':
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    body = self.rfile.read(content_length).decode('utf-8')
                    try:
                        data = json.loads(body)
                        
                        # Simple validation
                        if not data.get('name') or not data.get('email'):
                            self._send_json_response({"error": "Name and email are required"}, 400)
                            return
                        
                        # Email format validation
                        import re
                        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                        if not re.match(email_pattern, data['email']):
                            self._send_json_response({"error": "Invalid email format"}, 400)
                            return
                        
                        # Check if email already exists
                        if any(u['email'] == data['email'] for u in _db['users']):
                            self._send_json_response({"error": "Email already exists"}, 400)
                            return
                        
                        from datetime import datetime
                        new_user = {
                            'id': get_next_id('users'),
                            'name': data['name'],
                            'email': data['email'],
                            'created_at': datetime.utcnow().isoformat()
                        }
                        _db['users'].append(new_user)
                        self._send_json_response(new_user, 201)
                    except json.JSONDecodeError:
                        self._send_json_response({"error": "Invalid JSON"}, 400)
                    except Exception as e:
                        self._send_json_response({"error": str(e)}, 400)
                else:
                    self._send_json_response({"error": "No data provided"}, 400)
            else:
                self._send_json_response({"error": "Method not allowed"}, 405)
        except Exception as e:
            import traceback
            self._send_json_response({
                "error": f"Users endpoint error: {str(e)}",
                "traceback": traceback.format_exc()
            }, 500)
    
    def _handle_todos_endpoint(self, path):
        try:
            if self.command == 'GET':
                if path.endswith('/todos') or path.endswith('/todos/') or 'todos' in path and not any(char.isdigit() for char in path.split('todos')[-1]):
                    self._send_json_response(_db['todos'])
                else:
                    # Extract todo ID from path
                    parts = path.split('/')
                    todo_id_part = None
                    for i, part in enumerate(parts):
                        if part == 'todos' and i + 1 < len(parts):
                            todo_id_part = parts[i + 1]
                            break
                    
                    if todo_id_part:
                        try:
                            todo_id = int(todo_id_part)
                            todo = next((t for t in _db['todos'] if t['id'] == todo_id), None)
                            if todo:
                                self._send_json_response(todo)
                            else:
                                self._send_json_response({"error": "Todo not found"}, 404)
                        except ValueError:
                            self._send_json_response({"error": "Invalid todo ID"}, 400)
                    else:
                        self._send_json_response({"error": "Invalid path"}, 400)
            
            elif self.command == 'POST':
                content_length = int(self.headers.get('Content-Length', 0))
                if content_length > 0:
                    body = self.rfile.read(content_length).decode('utf-8')
                    try:
                        data = json.loads(body)
                        
                        # Simple validation
                        required_fields = ['title', 'description', 'user_id']
                        for field in required_fields:
                            if not data.get(field):
                                self._send_json_response({"error": f"{field} is required"}, 400)
                                return
                        
                        # Check if user exists
                        user = next((u for u in _db['users'] if u['id'] == data['user_id']), None)
                        if not user:
                            self._send_json_response({"error": "User not found"}, 400)
                            return
                        
                        from datetime import datetime
                        new_todo = {
                            'id': get_next_id('todos'),
                            'title': data['title'],
                            'description': data['description'],
                            'user_id': data['user_id'],
                            'completed': data.get('completed', False),
                            'created_at': datetime.utcnow().isoformat()
                        }
                        _db['todos'].append(new_todo)
                        self._send_json_response(new_todo, 201)
                    except json.JSONDecodeError:
                        self._send_json_response({"error": "Invalid JSON"}, 400)
                    except Exception as e:
                        self._send_json_response({"error": str(e)}, 400)
                else:
                    self._send_json_response({"error": "No data provided"}, 400)
            
            elif self.command == 'PUT':
                # Handle todo updates
                parts = path.split('/')
                todo_id_part = None
                for i, part in enumerate(parts):
                    if part == 'todos' and i + 1 < len(parts):
                        todo_id_part = parts[i + 1]
                        break
                
                if todo_id_part:
                    try:
                        todo_id = int(todo_id_part)
                        content_length = int(self.headers.get('Content-Length', 0))
                        if content_length > 0:
                            body = self.rfile.read(content_length).decode('utf-8')
                            try:
                                data = json.loads(body)
                                # Find and update todo
                                for i, todo in enumerate(_db['todos']):
                                    if todo['id'] == todo_id:
                                        for key, value in data.items():
                                            if key != 'id' and value is not None:
                                                _db['todos'][i][key] = value
                                        from datetime import datetime
                                        _db['todos'][i]['updated_at'] = datetime.utcnow().isoformat()
                                        self._send_json_response(_db['todos'][i])
                                        return
                                self._send_json_response({"error": "Todo not found"}, 404)
                            except json.JSONDecodeError:
                                self._send_json_response({"error": "Invalid JSON"}, 400)
                            except Exception as e:
                                self._send_json_response({"error": str(e)}, 400)
                        else:
                            self._send_json_response({"error": "No data provided"}, 400)
                    except ValueError:
                        self._send_json_response({"error": "Invalid todo ID"}, 400)
                else:
                    self._send_json_response({"error": "Invalid path"}, 400)
            else:
                self._send_json_response({"error": "Method not allowed"}, 405)
        except Exception as e:
            import traceback
            self._send_json_response({
                "error": f"Todos endpoint error: {str(e)}",
                "traceback": traceback.format_exc()
            }, 500)
    
    def _send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
