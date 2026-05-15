"""Template database model."""

from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


BEIJING_TZ = timezone(timedelta(hours=8))


def beijing_now() -> datetime:
    """Return current datetime in Beijing timezone."""
    return datetime.now(BEIJING_TZ).replace(tzinfo=None)


class Template(Base):
    """Represents a data generation template."""

    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        nullable=False,
        default="",
    )
    description: Mapped[str] = mapped_column(
        nullable=True,
        default=None,
    )
    fields: Mapped[str] = mapped_column(
        nullable=False,
        default="[]",
    )
    created_at: Mapped[datetime] = mapped_column(
        default=beijing_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=beijing_now,
        onupdate=beijing_now,
    )
