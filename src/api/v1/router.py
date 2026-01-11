"""API v1 router - Combines all v1 endpoints.

This router aggregates all v1 endpoints and provides a single
entry point for the v1 API.
"""

from fastapi import APIRouter

from src.api.v1.endpoints import tasks

# Create v1 API router
api_router = APIRouter()

# Include endpoint routers
api_router.include_router(tasks.router)

# Future endpoints can be added here:
# api_router.include_router(users.router)
# api_router.include_router(auth.router)
