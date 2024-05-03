"""HumanitarianNeeds table and view."""

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_dataset import DBDataset
from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.db_sector import DBSector
from hapi_schema.utils.base import Base
from hapi_schema.utils.shared_enums import (
    DisabledMarker,
    GenderMarker,
    PopulationGroup,
    PopulationStatus,
)
from hapi_schema.utils.view_params import ViewParams


class DBHumanitarianNeeds(Base):
    __tablename__ = "humanitarian_needs"
    __table_args__ = (
        CheckConstraint("population >= 0", name="population"),
        CheckConstraint(
            "(reference_period_end >= reference_period_start) OR (reference_period_start IS NULL)",
            name="reference_period",
        ),
    )

    resource_hdx_id: Mapped[str] = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"),
        primary_key=True,
    )
    population_status: Mapped[PopulationStatus] = mapped_column(
        Enum(PopulationStatus, name="population_status_enum"),
        primary_key=True,
    )
    population_group: Mapped[PopulationGroup] = mapped_column(
        Enum(PopulationGroup, name="population_group_enum"),
        primary_key=True,
    )
    sector_code: Mapped[str] = mapped_column(
        ForeignKey("sector.code", onupdate="CASCADE"),
        primary_key=True,
    )
    gender_marker: Mapped[GenderMarker] = mapped_column(
        Enum(GenderMarker, name="gender_marker_enum"), primary_key=True
    )
    age_range: Mapped[str] = mapped_column(String(32), primary_key=True)
    min_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    max_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    disabled_marker: Mapped[DisabledMarker] = mapped_column(
        Enum(DisabledMarker, name="disabled_marker_enum"), primary_key=True
    )
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime,
        primary_key=True,
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        server_default=text("NULL"),
        index=True,
    )

    resource = relationship("DBResource")
    admin2 = relationship("DBAdmin2")
    sector = relationship("DBSector")


view_params_humanitarian_needs = ViewParams(
    name="humanitarian_needs_view",
    metadata=Base.metadata,
    selectable=select(
        *DBHumanitarianNeeds.__table__.columns,
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
        DBAdmin1.location_ref.label("location_ref"),
        DBAdmin2.code.label("admin2_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.is_unspecified.label("admin2_is_unspecified"),
        DBAdmin2.admin1_ref.label("admin1_ref"),
        DBSector.name.label("sector_name"),
    ).select_from(
        # Join pop to admin2 to admin1 to loc
        DBHumanitarianNeeds.__table__.join(
            DBAdmin2.__table__,
            DBHumanitarianNeeds.admin2_ref == DBAdmin2.id,
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
        # Join needs to resource to dataset
        .join(
            DBResource.__table__,
            DBHumanitarianNeeds.resource_hdx_id == DBResource.hdx_id,
            isouter=True,
        )
        .join(
            DBDataset.__table__,
            DBResource.dataset_hdx_id == DBDataset.hdx_id,
            isouter=True,
        )
        # Join needs to sector
        .join(
            DBSector.__table__,
            DBHumanitarianNeeds.sector_code == DBSector.code,
            isouter=True,
        )
    ),
)
