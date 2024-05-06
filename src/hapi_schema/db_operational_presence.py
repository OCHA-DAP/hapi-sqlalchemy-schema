"""OperationalPresence table and view."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
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
from hapi_schema.db_org import DBOrg
from hapi_schema.db_org_type import DBOrgType
from hapi_schema.db_resource import DBResource
from hapi_schema.db_sector import DBSector
from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBOperationalPresence(Base):
    __tablename__ = "operational_presence"
    __table_args__ = (
        CheckConstraint(
            "(reference_period_end >= reference_period_start) OR (reference_period_start IS NULL)",
            name="reference_period",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_hdx_id = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"), nullable=False
    )
    org_ref: Mapped[str] = mapped_column(
        ForeignKey("org.id", onupdate="CASCADE"), nullable=False
    )
    sector_code: Mapped[str] = mapped_column(
        ForeignKey("sector.code", onupdate="CASCADE"), nullable=False
    )
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )
    source_data: Mapped[str] = mapped_column(Text, nullable=True)

    resource = relationship("DBResource")
    admin2 = relationship("DBAdmin2")
    org = relationship("DBOrg")
    sector = relationship("DBSector")


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
        DBOrg.acronym.label("org_acronym"),
        DBOrg.name.label("org_name"),
        DBOrg.org_type_code.label("org_type_code"),
        DBOrgType.description.label("org_type_description"),
        DBSector.name.label("sector_name"),
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
            DBOperationalPresence.resource_hdx_id == DBResource.hdx_id,
            isouter=True,
        )
        .join(
            DBDataset.__table__,
            DBResource.dataset_hdx_id == DBDataset.hdx_id,
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
        # Join op to sector
        .join(
            DBSector.__table__,
            DBOperationalPresence.sector_code == DBSector.code,
            isouter=True,
        )
    ),
)


class DBoperational_presence_vat(Base):
    __tablename__ = "operational_presence_vat"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin2_ref: Mapped[int] = mapped_column(Integer)
    org_ref: Mapped[int] = mapped_column(Integer)
    sector_code: Mapped[str] = mapped_column(String(32))
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
    location_ref: Mapped[int] = mapped_column(Integer)
    admin2_code: Mapped[str] = mapped_column(String(128))
    admin2_name: Mapped[str] = mapped_column(String(512))
    admin2_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    admin1_ref: Mapped[int] = mapped_column(Integer)
    org_acronym: Mapped[str] = mapped_column(String(32), index=True)
    org_name: Mapped[str] = mapped_column(String(512))
    org_type_code: Mapped[str] = mapped_column(String(32))
    org_type_description: Mapped[str] = mapped_column(String(512), index=True)
    sector_name: Mapped[str] = mapped_column(String(512), index=True)
