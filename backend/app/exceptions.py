"""Custom exceptions and global exception handler for the application."""

from fastapi import Request
from fastapi.responses import JSONResponse


class DataGenerationError(Exception):
    """Raised when data generation fails."""

    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class TemplateNotFoundError(Exception):
    """Raised when a requested template does not exist."""

    def __init__(self, template_id: str):
        self.template_id = template_id
        self.message = f"Template with id '{template_id}' not found"
        super().__init__(self.message)


class APIKeyError(Exception):
    """Raised when API key validation fails."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler to convert exceptions to JSON responses."""
    if isinstance(exc, TemplateNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"error": "not_found", "message": exc.message, "template_id": exc.template_id},
        )

    if isinstance(exc, APIKeyError):
        return JSONResponse(
            status_code=401,
            content={"error": "unauthorized", "message": exc.message},
        )

    if isinstance(exc, DataGenerationError):
        return JSONResponse(
            status_code=500,
            content={"error": "generation_failed", "message": exc.message, "details": exc.details},
        )

    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "message": str(exc)},
    )
