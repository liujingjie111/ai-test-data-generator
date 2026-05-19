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
    
    # 快速路径：直接检查 Origin
    if origin:
        return origin in settings.cors_origins
    
    # 如果没有 Origin，再检查 Referer（简单直接匹配）
    if referer:
        for allowed_origin in settings.cors_origins:
            if allowed_origin in referer:
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
