"""Location table and view."""
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, select, text
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


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


view_params_location = ViewParams(
    name="location_view",
    metadata=Base.metadata,
    selectable=select(*DBLocation.__table__.columns),
)
