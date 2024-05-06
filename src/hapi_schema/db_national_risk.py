"""NationalRisk table and view."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_dataset import DBDataset
from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBNationalRisk(Base):
    __tablename__ = "national_risk"
    __table_args__ = (
        CheckConstraint(
            "meta_avg_recentness_years >= 0.0",
            name="meta_avg_recentness_years",
        ),
        CheckConstraint(
            "(reference_period_end >= reference_period_start) OR (reference_period_start IS NULL)",
            name="reference_period",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_hdx_id: Mapped[int] = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"), nullable=False
    )
    risk_class: Mapped[int] = mapped_column(Integer, nullable=False)
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
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )
    source_data: Mapped[str] = mapped_column(Text, nullable=True)

    resource = relationship("DBResource")
    admin2 = relationship("DBAdmin2")


view_params_national_risk = ViewParams(
    name="national_risk_view",
    metadata=Base.metadata,
    selectable=select(
        *DBNationalRisk.__table__.columns,
        DBDataset.hdx_id.label("dataset_hdx_id"),
        DBDataset.hdx_stub.label("dataset_hdx_stub"),
        DBDataset.title.label("dataset_title"),
        DBDataset.hdx_provider_stub.label("dataset_hdx_provider_stub"),
        DBDataset.hdx_provider_name.label("dataset_hdx_provider_name"),
        DBResource.name.label("resource_name"),
        DBResource.update_date.label("resource_update_date"),
        DBResource.hapi_updated_date.label("hapi_updated_date"),
        DBResource.hapi_replaced_date.label("hapi_replaced_date"),
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


class DBnational_risk_vat(Base):
    __tablename__ = "national_risk_vat"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin2_ref: Mapped[int] = mapped_column(Integer)
    risk_class: Mapped[int] = mapped_column(Integer)
    global_rank: Mapped[int] = mapped_column(Integer)
    overall_risk: Mapped[float] = mapped_column(Float)
    hazard_exposure_risk: Mapped[float] = mapped_column(Float)
    vulnerability_risk: Mapped[float] = mapped_column(Float)
    coping_capacity_risk: Mapped[float] = mapped_column(Float)
    meta_missing_indicators_pct: Mapped[float] = mapped_column(Float)
    meta_avg_recentness_years: Mapped[float] = mapped_column(Float)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    source_data: Mapped[str] = mapped_column(Text)
    dataset_hdx_id: Mapped[str] = mapped_column(String(36))
    dataset_hdx_stub: Mapped[str] = mapped_column(String(128))
    dataset_title: Mapped[str] = mapped_column(String(1024))
    dataset_hdx_provider_stub: Mapped[str] = mapped_column(
        String(128), index=True
    )
    dataset_hdx_provider_name: Mapped[str] = mapped_column(
        String(512), index=True
    )
    resource_name: Mapped[str] = mapped_column(String(256))
    resource_update_date: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    hapi_updated_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    hapi_replaced_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    location_code: Mapped[str] = mapped_column(String(128))
    location_name: Mapped[str] = mapped_column(String(512))
    admin1_code: Mapped[str] = mapped_column(String(128))
    admin1_name: Mapped[str] = mapped_column(String(512))
    admin1_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    admin2_code: Mapped[str] = mapped_column(String(128))
    admin2_name: Mapped[str] = mapped_column(String(512))
    admin2_is_unspecified: Mapped[bool] = mapped_column(Boolean)
