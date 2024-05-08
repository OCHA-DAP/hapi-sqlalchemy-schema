"""OperationalPresence table and view."""

from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_location import DBLocation
from hapi_schema.db_org import DBOrg
from hapi_schema.db_sector import DBSector
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import reference_period_constraint
from hapi_schema.utils.view_params import ViewParams


class DBOperationalPresence(Base):
    __tablename__ = "operational_presence"
    # TODO: is there a better way?
    #  https://avacariu.me/writing/2019/composite-foreign-keys-and-many-to-many-relationships-in-sqlalchemy
    __table_args__ = (
        reference_period_constraint(),
        ForeignKeyConstraint(
            ["org_acronym", "org_name"],
            ["org.acronym", "org.name"],
        ),
    )

    resource_hdx_id = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"), primary_key=True
    )
    # Foreign key
    org_acronym: Mapped[str] = mapped_column(String, primary_key=True)
    # Foreign key
    org_name: Mapped[str] = mapped_column(String, primary_key=True)
    sector_code: Mapped[str] = mapped_column(
        ForeignKey("sector.code", onupdate="CASCADE"), primary_key=True
    )
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )

    resource = relationship("DBResource")
    admin2 = relationship("DBAdmin2")
    sector = relationship("DBSector")


view_params_operational_presence = ViewParams(
    name="operational_presence_view",
    metadata=Base.metadata,
    selectable=select(
        *DBOperationalPresence.__table__.columns,
        DBOrg.org_type_code.label("org_type_code"),
        DBSector.name.label("sector_name"),
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
        # Join to org
        .join(
            DBOrg.__table__,
            (DBOperationalPresence.org_name == DBOrg.name)
            & (DBOperationalPresence.org_acronym == DBOrg.acronym),
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
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin2_ref: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    org_acronym: Mapped[str] = mapped_column(String, primary_key=True)
    org_name: Mapped[str] = mapped_column(String, primary_key=True)
    sector_code: Mapped[str] = mapped_column(String(32))
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    org_type_code: Mapped[str] = mapped_column(String(32))
    sector_name: Mapped[str] = mapped_column(String(512))
    location_code: Mapped[str] = mapped_column(String(128))
    location_name: Mapped[str] = mapped_column(String(512), index=True)
    admin1_code: Mapped[str] = mapped_column(String(128))
    admin1_name: Mapped[str] = mapped_column(String(512))
    admin1_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    location_ref: Mapped[int] = mapped_column(Integer)
    admin2_code: Mapped[str] = mapped_column(String(128), index=True)
    admin2_name: Mapped[str] = mapped_column(String(512), index=True)
    admin2_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    admin1_ref: Mapped[int] = mapped_column(Integer)
