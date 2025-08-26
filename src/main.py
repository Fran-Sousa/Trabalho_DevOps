"""Main application file for the FastAPI web service."""
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    """Root endpoint returning a welcome message."""
    return "Welcome to Task Manager API"


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "ok"}
