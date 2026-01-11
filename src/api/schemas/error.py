"""Error response schemas for consistent API error handling."""

from pydantic import BaseModel


class ValidationErrorDetail(BaseModel):
    """Detailed validation error information for a specific field.

    Attributes:
        field: Name of the field that failed validation
        issue: Description of what went wrong
    """

    field: str
    issue: str


class ErrorResponse(BaseModel):
    """Standard error response format for all API errors.

    Attributes:
        code: Machine-readable error code (e.g., "VALIDATION_ERROR")
        message: Human-readable error message
        details: Optional list of detailed error information
    """

    code: str
    message: str
    details: list[ValidationErrorDetail] | None = None


class VersionConflictError(BaseModel):
    """Error response for optimistic locking version conflicts (409).

    Attributes:
        code: Always "VERSION_CONFLICT"
        message: Human-readable conflict explanation
        current_version: The actual current version in the database
        requested_version: The version the client tried to update
    """

    code: str = "VERSION_CONFLICT"
    message: str
    current_version: int
    requested_version: int
