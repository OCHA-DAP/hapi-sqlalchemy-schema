"""Gender table."""
from datetime import datetime

from hdx.database.no_timezone import Base
from sqlalchemy import DateTime, Integer, select, String, text
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.view import view


class DBLocation(Base):
    __tablename__ = "location"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL")
    )


location_view = view(
    name="location_view",
    metadata=Base.metadata,
    selectable=select(
        DBLocation.id,
        DBLocation.code,
        DBLocation.name,
        DBLocation.reference_period_start,
        DBLocation.reference_period_end,
    ),
)
