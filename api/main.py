"""
Main application entry point for Vercel serverless deployment.
This file creates the Sanic app and imports all modules to build the complete API.
"""

from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS
from modules.database import init_db
from modules.users import users_bp
from modules.todos import todos_bp
from modules.middleware import setup_middleware

def create_app() -> Sanic:
    """Create and configure the Sanic application."""
    app = Sanic("sanic_nextjs_template")
    
    # Enable CORS for frontend communication
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Setup middleware
    setup_middleware(app)
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.blueprint(users_bp, url_prefix="/api")
    app.blueprint(todos_bp, url_prefix="/api")
    
    # Health check endpoint
    @app.get("/api/health")
    async def health_check(request):
        return json({
            "status": "healthy",
            "message": "Sanic API is running",
            "version": "1.0.0"
        })
    
    # Root endpoint
    @app.get("/api")
    async def root(request):
        return json({
            "message": "Welcome to Sanic + Next.js Template API",
            "endpoints": {
                "health": "/api/health",
                "users": "/api/users",
                "todos": "/api/todos"
            }
        })
    
    return app

# Create the app instance for Vercel
app = create_app()

# For local development with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
