"""Location table and view."""

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Integer,
    String,
    UniqueConstraint,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBLocation(Base):
    __tablename__ = "location"
    __table_args__ = (
        CheckConstraint(
            "(reference_period_end >= reference_period_start) OR (reference_period_start IS NULL)",
            name="reference_period",
        ),
        CheckConstraint(
            "(hapi_replaced_date IS NULL) OR (hapi_replaced_date >= hapi_updated_date)",
            name="hapi_dates",
        ),
        UniqueConstraint("code", "hapi_updated_date", name="location_code_hapi_updated_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )
    hapi_updated_date = mapped_column(DateTime, nullable=False, index=True)
    hapi_replaced_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )


view_params_location = ViewParams(
    name="location_view",
    metadata=Base.metadata,
    selectable=select(*DBLocation.__table__.columns),
)
