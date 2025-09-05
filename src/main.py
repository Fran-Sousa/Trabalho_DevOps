"""Main application file for the FastAPI web service."""
from fastapi import FastAPI

from .routes import users

try:
    from .config import get_settings

    settings = get_settings()
    app = FastAPI(debug=settings.debug)
except ImportError:
    app = FastAPI()

# Include routers
app.include_router(users.router)


@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return "Welcome to Task Manager API"


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "ok"}
