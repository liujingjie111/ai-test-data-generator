"""FastAPI dependencies for database sessions and API key verification."""

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime

from app.config import settings
from app.database import get_db
from app.exceptions import APIKeyError
from app.models.api_key import ApiKey

security = HTTPBearer(auto_error=False)


def get_database_session(db: Session = Depends(get_db)) -> Session:
    """Dependency to provide a database session."""
    return db


def _is_allowed_origin(request: Request) -> bool:
    """Check if the request Origin is in the allowed CORS list."""
    origin = request.headers.get("origin")
    referer = request.headers.get("referer", "")
    
    print(f"DEBUG - Origin: {origin}, Referer: {referer}")
    print(f"DEBUG - Allowed origins: {settings.cors_origins}")
    
    # 只允许配置列表中的前端地址
    if origin:
        if origin in settings.cors_origins:
            print(f"DEBUG - Origin allowed (exact match): {origin}")
            return True
    
    if referer:
        for allowed_origin in settings.cors_origins:
            if allowed_origin in referer:
                print(f"DEBUG - Referer allowed: {referer}")
                return True
    
    return False


async def verify_api_key(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> str | None:
    """Dependency to verify the API key from the Authorization header.
    
    Allows requests from allowed CORS origins (frontend) without API key.
    Requires valid API key for all other requests.
    """
    if _is_allowed_origin(request):
        print(f"DEBUG - Request allowed without API key")
        return None
    
    if not credentials:
        raise APIKeyError("Missing API key. Provide Authorization: Bearer <your_api_key>")

    api_key = db.query(ApiKey).filter(
        ApiKey.key == credentials.credentials,
        ApiKey.is_active.is_(True),
    ).first()

    if not api_key:
        raise APIKeyError("Invalid API key")

    if api_key.expires_at and api_key.expires_at < datetime.utcnow():
        raise APIKeyError("API key has expired")

    return credentials.credentials


async def verify_api_key_required(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> str:
    """Dependency to verify the API key (required)."""
    if not credentials:
        raise APIKeyError("Missing API key")

    api_key = db.query(ApiKey).filter(
        ApiKey.key == credentials.credentials,
        ApiKey.is_active.is_(True),
    ).first()

    if not api_key:
        raise APIKeyError("Invalid API key")

    if api_key.expires_at and api_key.expires_at < datetime.utcnow():
        raise APIKeyError("API key has expired")

    return credentials.credentials
