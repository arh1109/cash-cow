"""
Day 4 - FastAPI application entrypoint

This file will control the entry point for our API. We build the FastAPI objects here
and register our various different routers to it for routing of our requests.
"""

from fastapi import FastAPI

from app.routers import atms, service_calls, auth


app = FastAPI(
    title="RoboPulse Fleet Command Center",
    description="Fleet Management API for Apex Robotics autonomous inspection rovers and aerial drones",
    version="0.1.0"
)

# Incude our routers in our API
app.include_router(atms.router)
app.include_router(service_calls.router)
app.include_router(auth.router)

# Sample health endpoint to validate the application is running correctly
@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}