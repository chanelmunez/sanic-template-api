"""
Middleware setup for the Sanic application.
"""

from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_middleware(app: Sanic) -> None:
    """Setup all middleware for the application."""
    
    @app.middleware("request")
    async def log_request(request: Request):
        """Log incoming requests."""
        request.ctx.start_time = time.time()
        logger.info(f"[{request.method}] {request.path} - {request.ip}")
    
    @app.middleware("response")
    async def log_response(request: Request, response: HTTPResponse):
        """Log outgoing responses with timing."""
        if hasattr(request.ctx, 'start_time'):
            duration = (time.time() - request.ctx.start_time) * 1000
            logger.info(f"[{request.method}] {request.path} - {response.status} - {duration:.2f}ms")
    
    @app.middleware("response")
    async def add_cors_headers(request: Request, response: HTTPResponse):
        """Add CORS headers to responses."""
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    
    @app.exception(Exception)
    async def handle_exception(request: Request, exception: Exception):
        """Global exception handler."""
        logger.error(f"Unhandled exception: {str(exception)}")
        from sanic.response import json
        return json({
            "error": "Internal server error",
            "message": str(exception) if app.debug else "An unexpected error occurred"
        }, status=500)
