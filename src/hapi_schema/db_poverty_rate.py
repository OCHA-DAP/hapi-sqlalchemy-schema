"""PovertyRate table and view."""

from datetime import datetime

from sqlalchemy import (
    Float,
    ForeignKey,
    String,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.sql import null
from sqlalchemy.sql.expression import literal

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    percentage_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.view_params import ViewParams


# normalised table
class DBPovertyRate(Base):
    __tablename__ = "poverty_rate"
    __table_args__ = (
        percentage_constraint(var_name="headcount_ratio"),
        percentage_constraint(var_name="intensity_of_deprivation"),
        percentage_constraint(var_name="vulnerable_to_poverty"),
        percentage_constraint(var_name="in_severe_poverty"),
        reference_period_constraint(),
        CheckConstraint(
            sqltext="ABS(headcount_ratio / 100 * intensity_of_deprivation / 100  - mpi) < 0.00001",
            name="mpi_product_constraint",
        ),
    )

    resource_hdx_id: Mapped[str] = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin1_ref: Mapped[int] = mapped_column(
        ForeignKey("admin1.id", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    provider_admin1_name: Mapped[str] = mapped_column(
        String(512), nullable=False, index=True, primary_key=True
    )
    mpi: Mapped[float] = mapped_column(Float, nullable=False, index=False)
    headcount_ratio: Mapped[float] = mapped_column(
        Float, nullable=False, index=False
    )
    intensity_of_deprivation: Mapped[float] = mapped_column(
        Float, nullable=False, index=False
    )
    vulnerable_to_poverty: Mapped[float] = mapped_column(
        Float, nullable=False, index=False
    )
    in_severe_poverty: Mapped[float] = mapped_column(
        Float, nullable=False, index=False
    )
    reference_period_start: Mapped[datetime] = mapped_column(primary_key=True)
    reference_period_end: Mapped[datetime] = mapped_column(
        nullable=False, index=True
    )

    resource = relationship(DBResource)
    admin1 = relationship(DBAdmin1)


# view
view_params_poverty_rate = ViewParams(
    name="poverty_rate_view",
    metadata=Base.metadata,
    selectable=select(
        *DBPovertyRate.__table__.columns,
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBLocation.has_hrp.label("has_hrp"),
        DBLocation.in_gho.label("in_gho"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin1.location_ref.label("location_ref"),
    ).select_from(
        # Join PR to admin1 to loc
        DBPovertyRate.__table__.join(
            DBAdmin1.__table__,
            DBPovertyRate.admin1_ref == DBAdmin1.id,
            isouter=True,
        ).join(
            DBLocation.__table__,
            DBAdmin1.location_ref == DBLocation.id,
            isouter=True,
        )
    ),
)

# Results format: category, subcategory, location_name, location_code, admin1_name, admin1_code, admin2_name, admin2_code, hapi_updated_date
availability_stmt_poverty_rate = (
    select(
        literal("population-social").label("category"),
        literal("poverty-rate").label("subcategory"),
        DBLocation.name.label("location_name"),
        DBLocation.code.label("location_code"),
        DBPovertyRate.provider_admin1_name.label(
            "admin1_name"
        ),  # fixme once we start p-coding
        null().label("admin1_code"),  # fixme once we start p-coding
        null().label("admin2_name"),
        null().label("admin2_code"),
        DBResource.hapi_updated_date,
    )
    .select_from(
        DBPovertyRate.__table__.join(
            DBAdmin1.__table__,
            DBPovertyRate.admin1_ref == DBAdmin1.id,
            isouter=True,
        )
        .join(
            DBLocation.__table__,
            DBAdmin1.location_ref == DBLocation.id,
            isouter=True,
        )
        .join(
            DBResource.__table__,
            DBPovertyRate.resource_hdx_id == DBResource.hdx_id,
        )
    )
    .distinct()
)
