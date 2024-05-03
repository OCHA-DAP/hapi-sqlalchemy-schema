"""Admin1 table and view."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_location import DBLocation
from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBAdmin1(Base):
    __tablename__ = "admin1"
    __table_args__ = (
        CheckConstraint(
            "(reference_period_end >= reference_period_start) OR (reference_period_start IS NULL)",
            name="reference_period",
        ),
        CheckConstraint(
            "(hapi_replaced_date IS NULL) OR (hapi_replaced_date >= hapi_updated_date)",
            name="hapi_dates",
        ),
        UniqueConstraint("code", "hapi_updated_date", name="admin1_code_hapi_updated_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    location_ref: Mapped[int] = mapped_column(
        ForeignKey("location.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    code: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    is_unspecified: Mapped[bool] = mapped_column(
        Boolean, server_default=text("FALSE")
    )
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

    location = relationship("DBLocation")


view_params_admin1 = ViewParams(
    name="admin1_view",
    metadata=Base.metadata,
    selectable=select(
        *DBAdmin1.__table__.columns,
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBLocation.reference_period_start.label(
            "location_reference_period_start"
        ),
        DBLocation.reference_period_end.label("location_reference_period_end"),
    ).select_from(
        DBAdmin1.__table__.join(
            DBLocation.__table__,
            DBAdmin1.location_ref == DBLocation.id,
            isouter=True,
        )
    ),
)
