"""FastAPI application initialization and configuration."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.schemas.error import ErrorResponse, ValidationErrorDetail
from src.database.connection import create_tables, engine
from src.utils.logging import logger


# Custom exception classes
class NotFoundError(Exception):
    """Raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)


class VersionConflictError(Exception):
    """Raised when optimistic locking version conflict occurs."""

    def __init__(self, message: str, current_version: int, requested_version: int):
        self.message = message
        self.current_version = current_version
        self.requested_version = requested_version
        super().__init__(self.message)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan events.

    Handles startup and shutdown events for the FastAPI application.

    Args:
        app: FastAPI application instance

    Yields:
        None
    """
    # Startup: Create database tables
    logger.info("Starting Task Management API")
    await create_tables()
    logger.info("Database tables created/verified")

    yield

    # Shutdown: Close database connections
    logger.info("Shutting down Task Management API")
    await engine.dispose()
    logger.info("Database connections closed")


# Create FastAPI app instance
app = FastAPI(
    title="Task Management API",
    description="REST API for managing tasks with full CRUD operations",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors (422 Unprocessable Entity).

    Args:
        request: HTTP request
        exc: Validation error exception

    Returns:
        JSON response with validation error details
    """
    details = [
        ValidationErrorDetail(
            field=".".join(str(loc) for loc in error["loc"]),
            issue=error["msg"],
        )
        for error in exc.errors()
    ]

    error_response = ErrorResponse(
        code="VALIDATION_ERROR",
        message="Request validation failed",
        details=details,
    )

    logger.warning(
        f"Validation error: {exc.errors()}", extra={"path": request.url.path}
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump(),
    )


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(
    request: Request, exc: NotFoundError
) -> JSONResponse:
    """Handle NotFoundError (404 Not Found).

    Args:
        request: HTTP request
        exc: Not found exception

    Returns:
        JSON response with error details
    """
    error_response = ErrorResponse(
        code="NOT_FOUND",
        message=exc.message,
    )

    logger.info(f"Resource not found: {exc.message}", extra={"path": request.url.path})

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error_response.model_dump(),
    )


@app.exception_handler(VersionConflictError)
async def version_conflict_exception_handler(
    request: Request, exc: VersionConflictError
) -> JSONResponse:
    """Handle VersionConflictError (409 Conflict).

    Args:
        request: HTTP request
        exc: Version conflict exception

    Returns:
        JSON response with conflict details
    """
    error_data = {
        "code": "VERSION_CONFLICT",
        "message": exc.message,
        "current_version": exc.current_version,
        "requested_version": exc.requested_version,
    }

    logger.warning(
        f"Version conflict: current={exc.current_version}, "
        f"requested={exc.requested_version}",
        extra={"path": request.url.path},
    )

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=error_data,
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions (500 Internal Server Error).

    Args:
        request: HTTP request
        exc: Unhandled exception

    Returns:
        JSON response with generic error message
    """
    error_response = ErrorResponse(
        code="INTERNAL_ERROR",
        message="An unexpected error occurred. Please try again later.",
    )

    logger.error(
        f"Unhandled exception: {str(exc)}",
        exc_info=True,
        extra={"path": request.url.path},
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str]:
    """Health check endpoint to verify API is running.

    Returns:
        dict: Status message
    """
    return {"status": "healthy"}


# Include API v1 router
from src.api.v1.router import api_router as v1_router

app.include_router(v1_router, prefix="/api/v1")
