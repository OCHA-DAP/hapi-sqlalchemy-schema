"""NationalRisk table and view."""
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_dataset import DBDataset
from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBNationalRisk(Base):
    __tablename__ = "national_risk"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_ref: Mapped[int] = mapped_column(
        ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    location_ref: Mapped[int] = mapped_column(
        ForeignKey("location.id", onupdate="CASCADE"), nullable=False
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
        DateTime, nullable=False, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL")
    )
    source_data: Mapped[str] = mapped_column(Text, nullable=True)

    resource = relationship("DBResource")
    location = relationship("DBLocation")


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
        DBResource.hdx_id.label("resource_hdx_id"),
        DBResource.name.label("resource_name"),
        DBResource.update_date.label("resource_update_date"),
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
    ).select_from(
        # Join risk to loc
        DBNationalRisk.__table__.join(
            DBLocation.__table__,
            DBNationalRisk.location_ref == DBLocation.id,
            isouter=True,
        )
        # Join risk to resource to dataset
        .join(
            DBResource.__table__,
            DBNationalRisk.resource_ref == DBResource.id,
            isouter=True,
        ).join(
            DBDataset.__table__,
            DBResource.dataset_ref == DBDataset.id,
            isouter=True,
        )
    ),
)
