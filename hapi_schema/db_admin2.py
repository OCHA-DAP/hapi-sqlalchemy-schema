"""Admin2 table and view."""
from datetime import datetime

from hdx.database.no_timezone import Base
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    select,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_location import DBLocation
from hapi_schema.view import view


class DBAdmin2(Base):
    __tablename__ = "admin2"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    admin1_ref: Mapped[int] = mapped_column(
        ForeignKey("admin1.id", onupdate="CASCADE", ondelete="CASCADE"),
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

    admin1 = relationship("DBAdmin1")


admin2_view = view(
    name="admin2_view",
    metadata=Base.metadata,
    selectable=select(
        *DBAdmin2.__table__.columns,
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin1.reference_period_start.label("admin1_reference_period_start"),
        DBAdmin1.reference_period_end.label("admin1_reference_period_end"),
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBLocation.reference_period_start.label(
            "location_reference_period_start"
        ),
        DBLocation.reference_period_end.label("location_reference_period_end"),
    ).select_from(
        DBAdmin2.__table__.join(
            DBAdmin1.__table__,
            DBAdmin2.admin1_ref == DBAdmin1.id,
            isouter=True,
        ).join(
            DBLocation.__table__,
            DBAdmin1.location_ref == DBLocation.id,
            isouter=True,
        ),
    ),
)
