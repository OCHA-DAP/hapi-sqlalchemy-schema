"""Admin2 table and view."""

from datetime import datetime

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

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_location import DBLocation
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    code_and_reference_period_unique_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.view_params import ViewParams


class DBAdmin2(Base):
    __tablename__ = "admin2"
    __table_args__ = (
        reference_period_constraint(),
        code_and_reference_period_unique_constraint(admin_level="admin2"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    admin1_ref: Mapped[int] = mapped_column(
        ForeignKey("admin1.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    code: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)
    is_unspecified: Mapped[bool] = mapped_column(
        Boolean, server_default=text("FALSE"), nullable=False
    )
    from_cods: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("TRUE")
    )
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )

    admin1 = relationship("DBAdmin1")


view_params_admin2 = ViewParams(
    name="admin2_view",
    metadata=Base.metadata,
    selectable=select(
        *DBAdmin2.__table__.columns,
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin1.location_ref.label("location_ref"),
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
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
