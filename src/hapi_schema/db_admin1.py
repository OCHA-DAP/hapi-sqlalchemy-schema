"""Admin1 table and view."""
from datetime import datetime

from hdx.database.no_timezone import Base
from hdx.database.views import view
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_location import DBLocation


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


admin1_view = view(
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
