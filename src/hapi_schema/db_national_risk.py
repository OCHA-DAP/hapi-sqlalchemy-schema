"""NationalRisk table and view."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_location import DBLocation
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    general_risk_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.enums import RiskClass
from hapi_schema.utils.view_params import ViewParams


class DBNationalRisk(Base):
    __tablename__ = "national_risk"
    __table_args__ = (
        general_risk_constraint("overall"),
        general_risk_constraint("hazard_exposure"),
        general_risk_constraint("vulnerability"),
        general_risk_constraint("coping_capacity"),
        CheckConstraint(
            "(global_rank >= 1) AND (global_rank <= 250)", name="global_rank"
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
        Enum(RiskClass), nullable=False
    )
    global_rank: Mapped[int] = mapped_column(Integer, nullable=False)
    overall_risk: Mapped[float] = mapped_column(Float, nullable=False)
    hazard_exposure_risk: Mapped[float] = mapped_column(Float, nullable=False)
    vulnerability_risk: Mapped[float] = mapped_column(Float, nullable=False)
    coping_capacity_risk: Mapped[float] = mapped_column(Float, nullable=False)
    meta_missing_indicators_pct: Mapped[float] = mapped_column(
        Float, nullable=True
    )
    meta_avg_recentness_years: Mapped[float] = mapped_column(
        Float, nullable=True
    )
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True
    )

    resource = relationship("DBResource")
    admin2 = relationship("DBLocation")


view_params_national_risk = ViewParams(
    name="national_risk_view",
    metadata=Base.metadata,
    selectable=select(
        *DBNationalRisk.__table__.columns,
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
    ).select_from(
        # Join risk to loc
        DBNationalRisk.__table__.join(
            DBLocation.__table__,
            DBNationalRisk.location_ref == DBLocation.id,
            isouter=True,
        )
    ),
)


class DBnational_risk_vat(Base):
    __tablename__ = "national_risk_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin2_ref: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    risk_class: Mapped[str] = mapped_column(String(9))
    global_rank: Mapped[int] = mapped_column(Integer)
    overall_risk: Mapped[float] = mapped_column(Float)
    hazard_exposure_risk: Mapped[float] = mapped_column(Float)
    vulnerability_risk: Mapped[float] = mapped_column(Float)
    coping_capacity_risk: Mapped[float] = mapped_column(Float)
    meta_missing_indicators_pct: Mapped[float] = mapped_column(Float)
    meta_avg_recentness_years: Mapped[float] = mapped_column(Float)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    location_code: Mapped[str] = mapped_column(String(128))
    location_name: Mapped[str] = mapped_column(String(512), index=True)
    admin1_code: Mapped[str] = mapped_column(String(128))
    admin1_name: Mapped[str] = mapped_column(String(512))
    admin1_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    admin2_code: Mapped[str] = mapped_column(String(128), index=True)
    admin2_name: Mapped[str] = mapped_column(String(512), index=True)
    admin2_is_unspecified: Mapped[bool] = mapped_column(Boolean)
