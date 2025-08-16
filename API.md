# API Documentation

Complete API reference for the Sanic backend.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-app.vercel.app`

## Authentication

Currently, the API does not require authentication. In production, you should implement:
- JWT tokens
- API keys
- OAuth integration

## Response Format

All API responses follow this structure:

### Success Response
```json
{
  "data": { ... },
  "status": "success"
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": "Additional error details",
  "status": "error"
}
```

## Health Check

### GET /api/health

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "Sanic API is running",
  "version": "1.0.0"
}
```

## Users API

### GET /api/users

Get all users.

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### GET /api/users/{id}

Get a specific user.

**Parameters:**
- `id` (integer): User ID

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `404`: User not found

### POST /api/users

Create a new user.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-01T00:00:00"
}
```

**Error Responses:**
- `400`: Validation error or email already exists

### PUT /api/users/{id}

Update a user.

**Parameters:**
- `id` (integer): User ID

**Request Body:**
```json
{
  "name": "Updated Name",
  "email": "updated@example.com"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Updated Name",
  "email": "updated@example.com",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### DELETE /api/users/{id}

Delete a user.

**Parameters:**
- `id` (integer): User ID

**Response:**
```json
{
  "message": "User deleted successfully"
}
```

## Todos API

### GET /api/todos

Get all todos with optional filtering.

**Query Parameters:**
- `user_id` (integer, optional): Filter by user ID
- `completed` (boolean, optional): Filter by completion status

**Response:**
```json
[
  {
    "id": 1,
    "title": "Sample Todo",
    "description": "This is a sample todo",
    "completed": false,
    "user_id": 1,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

### GET /api/todos/{id}

Get a specific todo.

**Parameters:**
- `id` (integer): Todo ID

**Response:**
```json
{
  "id": 1,
  "title": "Sample Todo",
  "description": "This is a sample todo",
  "completed": false,
  "user_id": 1,
  "created_at": "2024-01-01T00:00:00"
}
```

### POST /api/todos

Create a new todo.

**Request Body:**
```json
{
  "title": "New Todo",
  "description": "Todo description",
  "user_id": 1,
  "completed": false
}
```

**Response:**
```json
{
  "id": 1,
  "title": "New Todo",
  "description": "Todo description",
  "completed": false,
  "user_id": 1,
  "created_at": "2024-01-01T00:00:00"
}
```

### PUT /api/todos/{id}

Update a todo.

**Parameters:**
- `id` (integer): Todo ID

**Request Body:**
```json
{
  "title": "Updated Todo",
  "description": "Updated description",
  "completed": true
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Todo",
  "description": "Updated description",
  "completed": true,
  "user_id": 1,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

### DELETE /api/todos/{id}

Delete a todo.

**Parameters:**
- `id` (integer): Todo ID

**Response:**
```json
{
  "message": "Todo deleted successfully"
}
```

### GET /api/users/{id}/todos

Get all todos for a specific user.

**Parameters:**
- `id` (integer): User ID

**Response:**
```json
[
  {
    "id": 1,
    "title": "User's Todo",
    "description": "This todo belongs to the user",
    "completed": false,
    "user_id": 1,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

## Error Codes

| Code | Description |
|------|-------------|
| 200  | Success |
| 201  | Created |
| 400  | Bad Request / Validation Error |
| 404  | Not Found |
| 500  | Internal Server Error |

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:
- Implementing rate limiting middleware
- Using external services like Upstash Redis
- Setting appropriate limits per endpoint

## Examples

### cURL Examples

**Get all users:**
```bash
curl https://your-app.vercel.app/api/users
```

**Create a user:**
```bash
curl -X POST https://your-app.vercel.app/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com"}'
```

**Create a todo:**
```bash
curl -X POST https://your-app.vercel.app/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title":"New Todo","description":"Description","user_id":1}'
```

### JavaScript Examples

**Using fetch:**
```javascript
// Get users
const users = await fetch('/api/python/users').then(r => r.json());

// Create user
const newUser = await fetch('/api/python/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'John', email: 'john@example.com' })
}).then(r => r.json());
```

**Using axios:**
```javascript
// Get todos
const todos = await axios.get('/api/python/todos');

// Update todo
await axios.put(`/api/python/todos/${todoId}`, {
  completed: true
});
```
