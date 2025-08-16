"""
Vercel serverless function handler.
This file adapts the Sanic ASGI app to work with Vercel's serverless infrastructure.
"""

from main import app

# Export the app for Vercel
application = app

# Vercel expects a handler function
def handler(event, context):
    """Handler function for Vercel serverless deployment."""
    return app(event, context)
