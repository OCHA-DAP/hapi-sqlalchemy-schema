"""OperationalPresence table and view."""
from datetime import datetime

from sqlalchemy import (
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
from hapi_schema.db_location import DBLocation
from hapi_schema.db_org import DBOrg
from hapi_schema.db_org_type import DBOrgType
from hapi_schema.db_resource import DBResource
from hapi_schema.db_sector import DBSector
from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBOperationalPresence(Base):
    __tablename__ = "operational_presence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_ref = mapped_column(
        ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"), nullable=False
    )
    sector_code: Mapped[str] = mapped_column(
        ForeignKey("sector.code", onupdate="CASCADE"), nullable=False
    )
    org_ref: Mapped[str] = mapped_column(
        ForeignKey("org.id", onupdate="CASCADE"), nullable=False
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
    sector = relationship("DBSector")
    org = relationship("DBOrg")


view_params_operational_presence = ViewParams(
    name="operational_presence_view",
    metadata=Base.metadata,
    selectable=select(
        *DBOperationalPresence.__table__.columns,
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
        DBSector.name.label("sector_name"),
        DBOrg.acronym.label("org_acronym"),
        DBOrg.name.label("org_name"),
        DBOrg.org_type_code.label("org_type_code"),
        DBOrgType.description.label("org_type_description")
    ).select_from(
        # Join op to admin2 to admin1 to loc
        DBOperationalPresence.__table__.join(
            DBAdmin2.__table__,
            DBOperationalPresence.admin2_ref == DBAdmin2.id,
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
        # Join op to resource to dataset
        .join(
            DBResource.__table__,
            DBOperationalPresence.resource_ref == DBResource.id,
            isouter=True,
        )
        .join(
            DBDataset.__table__,
            DBResource.dataset_ref == DBDataset.id,
            isouter=True,
        )
        # Join op to sector
        .join(
            DBSector.__table__,
            DBOperationalPresence.sector_code == DBSector.code,
            isouter=True,
        )
        # Join op to org to org type
        .join(
            DBOrg.__table__,
            DBOperationalPresence.org_ref == DBOrg.id,
            isouter=True,
        )
        .join(
            DBOrgType.__table__,
            DBOrg.org_type_code == DBOrgType.code,
            isouter=True,
        )
    ),
)
