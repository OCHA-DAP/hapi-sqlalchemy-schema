"""NationalRisk table and view."""

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    Text,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_dataset import DBDataset
from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
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
            "meta_avg_recentness_years >= 0.0",
            name="meta_avg_recentness_years",
        ),
        CheckConstraint(
            "(meta_missing_indicators_pct >= 0.0) AND (meta_missing_indicators_pct <= 10.0)",
            name="meta_missing_indicators_pct",
        ),
        reference_period_constraint(),
    )

    resource_hdx_id: Mapped[int] = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"), primary_key=True
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
    source_data: Mapped[str] = mapped_column(Text, nullable=True)

    resource = relationship("DBResource")
    admin2 = relationship("DBAdmin2")


view_params_national_risk = ViewParams(
    name="national_risk_view",
    metadata=Base.metadata,
    selectable=select(
        *DBNationalRisk.__table__.columns,
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin2.code.label("admin2_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.is_unspecified.label("admin2_is_unspecified"),
    ).select_from(
        # Join risk to admin 2 to admin 1 to loc
        DBNationalRisk.__table__.join(
            DBAdmin2.__table__,
            DBNationalRisk.admin2_ref == DBAdmin2.id,
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
        # Join risk to resource to dataset
        .join(
            DBResource.__table__,
            DBNationalRisk.resource_hdx_id == DBResource.hdx_id,
            isouter=True,
        )
        .join(
            DBDataset.__table__,
            DBResource.dataset_hdx_id == DBDataset.hdx_id,
            isouter=True,
        )
    ),
)
