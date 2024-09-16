"""NationalRisk table and view."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Float,
    ForeignKey,
    Integer,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import literal

from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    general_risk_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.enums import RiskClass, build_enum_using_values
from hapi_schema.utils.view_params import ViewParams


class DBNationalRisk(Base):
    __tablename__ = "national_risk"
    __table_args__ = (
        general_risk_constraint("overall"),
        general_risk_constraint("hazard_exposure"),
        general_risk_constraint("vulnerability"),
        general_risk_constraint("coping_capacity"),
        CheckConstraint(
            "(global_rank >= 1) AND (global_rank <= 250)",
            name="global_rank_constraint",
        ),
        CheckConstraint(
            "meta_avg_recentness_years >= 0.0",
            name="meta_avg_recentness_years",
        ),
        CheckConstraint(
            "(meta_missing_indicators_pct >= 0.0) AND (meta_missing_indicators_pct <= 100.0)",
            name="meta_missing_indicators_pct",
        ),
        reference_period_constraint(),
    )

    resource_hdx_id: Mapped[str] = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    location_ref: Mapped[int] = mapped_column(
        ForeignKey("location.id", onupdate="CASCADE"), primary_key=True
    )
    risk_class: Mapped[RiskClass] = mapped_column(
        build_enum_using_values(RiskClass), nullable=False
    )
    global_rank: Mapped[int] = mapped_column(Integer, nullable=False)
    overall_risk: Mapped[Decimal] = mapped_column(Float, nullable=False)
    hazard_exposure_risk: Mapped[Decimal] = mapped_column(
        Float, nullable=False
    )
    vulnerability_risk: Mapped[Decimal] = mapped_column(Float, nullable=False)
    coping_capacity_risk: Mapped[Decimal] = mapped_column(
        Float, nullable=False
    )
    meta_missing_indicators_pct: Mapped[Decimal] = mapped_column(
        Float, nullable=True
    )
    meta_avg_recentness_years: Mapped[Decimal] = mapped_column(
        Float, nullable=True
    )
    reference_period_start: Mapped[datetime] = mapped_column(primary_key=True)
    reference_period_end: Mapped[datetime] = mapped_column(
        nullable=False, index=True
    )

    resource = relationship(DBResource)
    location = relationship(DBLocation)


view_params_national_risk = ViewParams(
    name="national_risk_view",
    metadata=Base.metadata,
    selectable=select(
        *DBNationalRisk.__table__.columns,
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBLocation.has_hrp.label("has_hrp"),
        DBLocation.in_gho.label("in_gho"),
    ).select_from(
        # Join risk to loc
        DBNationalRisk.__table__.join(
            DBLocation.__table__,
            DBNationalRisk.location_ref == DBLocation.id,
            isouter=True,
        )
    ),
)

# Results format: category, subcategory, location_name, location_code, admin1_name, admin1_code, admin2_name, admin2_code, hapi_updated_date
availability_stmt_national_risk = (
    select(
        literal("coordination-context").label("category"),
        literal("national-risk").label("subcategory"),
        DBLocation.name.label("location_name"),
        DBLocation.code.label("location_code"),
        literal("").label("admin1_name"),
        literal("").label("admin1_code"),
        literal("").label("admin2_name"),
        literal("").label("admin2_code"),
        DBResource.hapi_updated_date,
    )
    .select_from(
        DBNationalRisk.__table__.join(
            DBLocation.__table__,
            DBNationalRisk.location_ref == DBLocation.id,
            isouter=True,
        ).join(
            DBResource.__table__,
            DBNationalRisk.resource_hdx_id == DBResource.hdx_id,
        )
    )
    .distinct()
)
