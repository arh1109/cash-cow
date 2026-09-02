"""
Day 4 - FastAPI application entrypoint

This file will control the entry point for our API. We build the FastAPI objects here
and register our various different routers to it for routing of our requests.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import atms, service_calls, auth


app = FastAPI(
    title="CashCow Branch Operations Command Center",
    description="Branch Operations Command Center API for Meridian Trust Bank's shared pool of ATMs",
    version="0.1.0"
)

#CORS Configuration
app.add_middleware(
    CORSMiddleware,
    #The endpoint for our frontent, currently provided by the vite dev server
    allow_origins=["http://localhost:5173"],
    #This allows us to pass an Authorization header (JWT)
    allow_credentials=True,
    #This allows all methods and headers through
    allow_methods=["*"],
    allow_headers=["*"]
)

# Incude our routers in our API
app.include_router(atms.router)
app.include_router(service_calls.router)
app.include_router(auth.router)

# Sample health endpoint to validate the application is running correctly
@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}