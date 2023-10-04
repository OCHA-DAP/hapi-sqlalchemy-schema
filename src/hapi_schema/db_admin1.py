"""Admin1 table."""
from datetime import datetime

from hdx.database.no_timezone import Base
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_location import DBLocation  # noqa: F401


class DBAdmin1(Base):
    __tablename__ = "admin1"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    location_ref: Mapped[int] = mapped_column(
        ForeignKey("location.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    code: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    is_unspecified: Mapped[bool] = mapped_column(
        Boolean, server_default=text("FALSE")
    )
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=False
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL")
    )

    location = relationship("DBLocation")
