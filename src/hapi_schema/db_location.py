"""Location table and view."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    code_and_reference_period_unique_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.view_params import ViewParams


class DBLocation(Base):
    __tablename__ = "location"
    __table_args__ = (
        reference_period_constraint(),
        code_and_reference_period_unique_constraint(admin_level="location"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    from_cods: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("TRUE")
    )
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )


view_params_location = ViewParams(
    name="location_view",
    metadata=Base.metadata,
    selectable=select(*DBLocation.__table__.columns),
)
