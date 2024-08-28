"""IDPs subcategory table and view."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import null
from sqlalchemy.sql.expression import literal

from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import reference_period_constraint
from hapi_schema.utils.view_params import ViewParams


class DBIDPs(Base):
    __tablename__ = "idps"
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

    appeal_type: Mapped[str] = mapped_column(String(32), nullable=False)

    requirements_usd: Mapped[Decimal] = mapped_column(
        nullable=False, index=True
    )

    funding_usd: Mapped[Decimal] = mapped_column(nullable=False, index=True)

    funding_pct: Mapped[Decimal] = mapped_column(nullable=False, index=True)

    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime,
        primary_key=True,
    )

    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        server_default=text("NULL"),
    )

    resource = relationship(DBResource)
    location = relationship(DBLocation)


view_params_idps = ViewParams(
    name="idps_view",
    metadata=Base.metadata,
    selectable=select(
        *DBIDPs.__table__.columns,
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBLocation.has_hrp.label("has_hrp"),
        DBLocation.in_gho.label("in_gho"),
    ).select_from(
        DBIDPs.__table__.join(
            DBLocation.__table__,
            DBIDPs.location_ref == DBLocation.id,
            isouter=True,
        )
    ),
)

# Results format: category, subcategory, location_name, location_code, admin1_name, admin1_code, admin2_name, admin2_code, hapi_updated_date
availability_stmt_idps = (
    select(
        literal("coordination-context").label("category"),
        literal("idps").label("subcategory"),
        DBLocation.name.label("location_name"),
        DBLocation.code.label("location_code"),
        null().label("admin1_name"),
        null().label("admin1_code"),
        null().label("admin2_name"),
        null().label("admin2_code"),
        DBResource.hapi_updated_date,
    )
    .select_from(
        DBIDPs.__table__.join(
            DBLocation.__table__,
            DBIDPs.location_ref == DBLocation.id,
            isouter=True,
        ).join(
            DBResource.__table__,
            DBIDPs.resource_hdx_id == DBResource.hdx_id,
        )
    )
    .distinct()
)
