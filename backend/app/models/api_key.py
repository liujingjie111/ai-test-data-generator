"""API Key database model."""

from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


BEIJING_TZ = timezone(timedelta(hours=8))


def beijing_now() -> datetime:
    """Return current datetime in Beijing timezone."""
    return datetime.now(BEIJING_TZ).replace(tzinfo=None)


class ApiKey(Base):
    """Represents an API authentication key."""

    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str] = mapped_column(
        nullable=False,
        unique=True,
    )
    name: Mapped[str] = mapped_column(
        nullable=False,
        default="",
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=beijing_now,
    )
    expires_at: Mapped[datetime] = mapped_column(
        nullable=True,
        default=None,
    )
