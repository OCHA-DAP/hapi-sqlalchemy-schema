"""Rainfall table and view."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import literal

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.utils import endpoint_constants
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    greater_than_constraint,
    non_negative_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.enums import (
    AggregationPeriod,
    Version,
    build_enum_using_values,
)
from hapi_schema.utils.view_params import ViewParams
from hapi_schema.views import get_admin2_case_code


class DBRainfall(Base):
    __tablename__ = "rainfall"
    __table_args__ = (
        greater_than_constraint("number_pixels", 1),
        non_negative_constraint(var_name="rainfall"),
        non_negative_constraint(var_name="rainfall_long_term_average"),
        non_negative_constraint(var_name="rainfall_anomaly_pct"),
        reference_period_constraint(),
    )

    resource_hdx_id: Mapped[str] = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"),
        primary_key=True,
    )
    provider_admin1_code = mapped_column(String(512), primary_key=True)
    provider_admin2_code = mapped_column(String(512), primary_key=True)
    aggregation_period: Mapped[AggregationPeriod] = mapped_column(
        build_enum_using_values(AggregationPeriod), primary_key=True
    )
    rainfall: Mapped[Decimal] = mapped_column(nullable=False)
    rainfall_long_term_average: Mapped[Decimal] = mapped_column(nullable=False)
    rainfall_anomaly_pct: Mapped[Decimal] = mapped_column(nullable=False)
    number_pixels: Mapped[int] = mapped_column(Integer, nullable=False)
    version: Mapped[Version] = mapped_column(
        build_enum_using_values(Version), primary_key=True
    )
    reference_period_start: Mapped[datetime] = mapped_column(
        nullable=False, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        nullable=False, index=True
    )

    resource = relationship(DBResource)
    admin2 = relationship(DBAdmin2)


view_params_rainfall = ViewParams(
    name="rainfall_view",
    metadata=Base.metadata,
    selectable=select(
        *DBRainfall.__table__.columns,
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBLocation.has_hrp.label("has_hrp"),
        DBLocation.in_gho.label("in_gho"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin1.location_ref.label("location_ref"),
        DBAdmin2.code.label("admin2_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.is_unspecified.label("admin2_is_unspecified"),
        DBAdmin2.admin1_ref.label("admin1_ref"),
        get_admin2_case_code(DBRainfall),
    ).select_from(
        # Join pop to admin2 to admin1 to loc
        DBRainfall.__table__.join(
            DBAdmin2.__table__,
            DBRainfall.admin2_ref == DBAdmin2.id,
            isouter=True,
        )
        .join(
            DBAdmin1.__table__,
            DBAdmin2.admin1_ref == DBAdmin1.id,
            isouter=True,
        )
        .join(
            DBLocation.__table__,
            DBAdmin1.location_ref == DBLocation.id,
            isouter=True,
        )
    ),
)

# Results format: category, subcategory, location_name, location_code, admin1_name, admin1_code, admin2_name, admin2_code, hapi_updated_date
availability_stmt_rainfall = (
    select(
        literal(endpoint_constants.RAINFALL_CAT).label("category"),
        literal(endpoint_constants.RAINFALL_SUBCAT).label("subcategory"),
        DBLocation.name.label("location_name"),
        DBLocation.code.label("location_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.code.label("admin2_code"),
        get_admin2_case_code(DBRainfall),
        DBResource.hapi_updated_date,
    )
    .select_from(
        DBRainfall.__table__.join(
            DBAdmin2.__table__,
            DBRainfall.admin2_ref == DBAdmin2.id,
            isouter=True,
        )
        .join(
            DBAdmin1.__table__,
            DBAdmin2.admin1_ref == DBAdmin1.id,
            isouter=True,
        )
        .join(
            DBLocation.__table__,
            DBAdmin1.location_ref == DBLocation.id,
            isouter=True,
        )
        .join(
            DBResource.__table__,
            DBRainfall.resource_hdx_id == DBResource.hdx_id,
        )
    )
    .distinct()
)
