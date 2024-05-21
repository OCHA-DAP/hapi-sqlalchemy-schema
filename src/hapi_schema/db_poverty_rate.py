"""PovertyRate table and view."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    String,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    rate_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.enums import PovertyClassification
from hapi_schema.utils.view_params import ViewParams


# normalised table
class DBPovertyRate(Base):
    __tablename__ = "poverty_rate"
    __table_args__ = (
        rate_constraint(),
        reference_period_constraint(),
    )

    resource_hdx_id: Mapped[str] = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    location_ref: Mapped[int] = mapped_column(
        ForeignKey("location.id", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    admin1_name: Mapped[str] = mapped_column(
        String(512), nullable=False, index=True, primary_key=True
    )
    classification: Mapped[PovertyClassification] = mapped_column(
        Enum(PovertyClassification), nullable=False, primary_key=True
    )
    rate: Mapped[Decimal] = mapped_column(nullable=True, index=False)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True
    )

    resource = relationship(DBResource)
    location = relationship(DBLocation)


# view
view_params_poverty_rate = ViewParams(
    name="poverty_rate_view",
    metadata=Base.metadata,
    selectable=select(
        *DBPovertyRate.__table__.columns,
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
    ).select_from(
        DBPovertyRate.__table__.join(
            DBLocation.__table__,
            DBPovertyRate.location_ref == DBLocation.id,
            isouter=True,
        )
    ),
)
