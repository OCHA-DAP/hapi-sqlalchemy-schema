"""HumanitarianNeeds table and view."""
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_dataset import DBDataset
from hapi_schema.db_gender import DBGender
from hapi_schema.db_location import DBLocation
from hapi_schema.db_population_group import DBPopulationGroup
from hapi_schema.db_population_status import DBPopulationStatus
from hapi_schema.db_resource import DBResource
from hapi_schema.db_sector import DBSector
from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBHumanitarianNeeds(Base):
    __tablename__ = "humanitarian_needs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_ref: Mapped[int] = mapped_column(
        ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"), nullable=False
    )
    gender_code: Mapped[str] = mapped_column(
        ForeignKey("gender.code", onupdate="CASCADE"), nullable=True
    )
    age_range_code: Mapped[str] = mapped_column(
        ForeignKey("age_range.code", onupdate="CASCADE"), nullable=True
    )
    disabled_marker: Mapped[bool] = mapped_column(
        Boolean, nullable=True, server_default=text("NULL")
    )
    sector_code: Mapped[str] = mapped_column(
        ForeignKey("sector.code", onupdate="CASCADE"), nullable=True
    )
    population_group_code: Mapped[str] = mapped_column(
        ForeignKey("population_group.code", onupdate="CASCADE"), nullable=True
    )
    population_status_code: Mapped[str] = mapped_column(
        ForeignKey("population_status.code", onupdate="CASCADE"),
        nullable=False,
    )
    population: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL")
    )
    source_data: Mapped[str] = mapped_column(Text, nullable=True)

    resource = relationship("DBResource")
    admin2 = relationship("DBAdmin2")
    gender = relationship("DBGender")
    age_range = relationship("DBAgeRange")
    sector = relationship("DBSector")
    population_group = relationship("DBPopulationGroup")
    population_status = relationship("DBPopulationStatus")


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
        DBResource.hdx_id.label("resource_hdx_id"),
        DBResource.name.label("resource_name"),
        DBResource.update_date.label("resource_update_date"),
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin2.code.label("admin2_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.is_unspecified.label("admin2_is_unspecified"),
        DBGender.description.label("gender_description"),
        DBSector.name.label("sector_name"),
        DBPopulationGroup.description.label("population_group_description"),
        DBPopulationStatus.description.label("population_status_description"),
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
            DBHumanitarianNeeds.resource_ref == DBResource.id,
            isouter=True,
        )
        .join(
            DBDataset.__table__,
            DBResource.dataset_ref == DBDataset.id,
            isouter=True,
        )
        # Join needs to gender
        .join(
            DBGender.__table__,
            DBHumanitarianNeeds.gender_code == DBGender.code,
            isouter=True,
        )
        # Join needs to sector
        .join(
            DBSector.__table__,
            DBHumanitarianNeeds.sector_code == DBSector.code,
            isouter=True,
        )
        # Join needs to pop group
        .join(
            DBPopulationGroup.__table__,
            DBHumanitarianNeeds.population_group_code
            == DBPopulationGroup.code,
            isouter=True,
        )
        # Join needs to pop status
        .join(
            DBPopulationStatus.__table__,
            DBHumanitarianNeeds.population_status_code
            == DBPopulationStatus.code,
            isouter=True,
        )
    ),
)
