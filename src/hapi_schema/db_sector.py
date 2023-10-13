"""Sector table and view."""
from datetime import datetime

from sqlalchemy import DateTime, String, select, text
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.base import Base


class DBSector(Base):
    __tablename__ = "sector"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL")
    )


sector_view_params = dict(
    name="sector_view",
    metadata=Base.metadata,
    selectable=select(*DBSector.__table__.columns),
)
