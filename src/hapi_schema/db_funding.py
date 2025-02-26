"""Funding subcategory table and view."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import literal

from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.utils import endpoint_constants
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import reference_period_constraint
from hapi_schema.utils.view_params import ViewParams


class DBFunding(Base):
    __tablename__ = "funding"
    __table_args__ = (
        CheckConstraint(
            "requirements_usd >= 0.0",
            name="requirements_usd_constraint",
        ),
        CheckConstraint(
            "funding_usd >= 0.0",
            name="funding_usd_constraint",
        ),
        CheckConstraint(
            "funding_pct >= 0.0",
            name="funding_pct_constraint",
        ),
        reference_period_constraint(),
    )

    resource_hdx_id = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )

    appeal_code: Mapped[str] = mapped_column(
        String(32),
        primary_key=True,
    )

    location_ref: Mapped[int] = mapped_column(
        ForeignKey("location.id", onupdate="CASCADE"),
        primary_key=True,
    )

    appeal_name: Mapped[str] = mapped_column(String(256), nullable=False)

    appeal_type: Mapped[str] = mapped_column(String(32), nullable=True)

    requirements_usd: Mapped[Decimal] = mapped_column(
        nullable=True, index=True
    )

    funding_usd: Mapped[Decimal] = mapped_column(nullable=False, index=True)

    funding_pct: Mapped[Decimal] = mapped_column(nullable=True, index=True)

    reference_period_start: Mapped[datetime] = mapped_column(
        primary_key=True,
    )

    reference_period_end: Mapped[datetime] = mapped_column(
        nullable=False, index=True
    )

    resource = relationship(DBResource)
    location = relationship(DBLocation)


view_params_funding = ViewParams(
    name="funding_view",
    metadata=Base.metadata,
    selectable=select(
        *DBFunding.__table__.columns,
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBLocation.has_hrp.label("has_hrp"),
        DBLocation.in_gho.label("in_gho"),
    ).select_from(
        DBFunding.__table__.join(
            DBLocation.__table__,
            DBFunding.location_ref == DBLocation.id,
            isouter=True,
        )
    ),
)

# Results format: category, subcategory, location_name, location_code, admin1_name, admin1_code, admin2_name, admin2_code, hapi_updated_date
availability_stmt_funding = (
    select(
        literal(endpoint_constants.FUNDING_CAT).label("category"),
        literal(endpoint_constants.FUNDING_SUBCAT).label("subcategory"),
        DBLocation.name.label("location_name"),
        DBLocation.code.label("location_code"),
        literal("").label("admin1_name"),
        literal("").label("admin1_code"),
        literal("").label("admin2_name"),
        literal("").label("admin2_code"),
        literal(0).label("admin_level"),
        DBResource.hapi_updated_date,
    )
    .select_from(
        DBFunding.__table__.join(
            DBLocation.__table__,
            DBFunding.location_ref == DBLocation.id,
            isouter=True,
        ).join(
            DBResource.__table__,
            DBFunding.resource_hdx_id == DBResource.hdx_id,
        )
    )
    .distinct()
)
