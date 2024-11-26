"""OperationalPresence table and view."""

from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    ForeignKeyConstraint,
    String,
    case,
    or_,
    select,
    text, and_,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import literal

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_location import DBLocation
from hapi_schema.db_org import DBOrg, DBOrgType
from hapi_schema.db_resource import DBResource
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
    provider_admin1_name = mapped_column(String(512), primary_key=True)
    provider_admin2_name = mapped_column(String(512), primary_key=True)
    # Foreign key
    org_acronym: Mapped[str] = mapped_column(String, primary_key=True)
    # Foreign key
    org_name: Mapped[str] = mapped_column(String, primary_key=True)
    sector_code: Mapped[str] = mapped_column(
        ForeignKey("sector.code", onupdate="CASCADE"), primary_key=True
    )
    reference_period_start: Mapped[datetime] = mapped_column(primary_key=True)
    reference_period_end: Mapped[datetime] = mapped_column(
        nullable=True, server_default=text("NULL"), index=True
    )

    resource = relationship(DBResource)
    admin2 = relationship(DBAdmin2)
    sector = relationship(DBSector)


view_params_operational_presence = ViewParams(
    name="operational_presence_view",
    metadata=Base.metadata,
    selectable=select(
        *DBOperationalPresence.__table__.columns,
        DBOrg.org_type_code.label("org_type_code"),
        DBOrgType.description.label("org_type_description"),
        DBSector.name.label("sector_name"),
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBLocation.has_hrp.label("has_hrp"),
        DBLocation.in_gho.label("in_gho"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin1.location_ref.label("location_ref"),
        DBAdmin2.code.label("admin2_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.is_unspecified.label("admin2_is_unspecified"),
        DBAdmin2.admin1_ref.label("admin1_ref"),
        case(
            (
                or_(
                    and_(DBOperationalPresence.provider_admin2_name.is_not(None), DBOperationalPresence.provider_admin2_name != ""),
                    DBAdmin2.is_unspecified.is_(False),
                ),
                2,
            ),
            (
                or_(
                    and_(DBOperationalPresence.provider_admin1_name.is_not(None), DBOperationalPresence.provider_admin1_name != ""),
                    DBAdmin1.is_unspecified.is_(False),
                ),
                1,
            ),
            else_=0,
        ).label("admin_level"),
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
        # Join org to org_type
        .join(
            DBOrgType.__table__,
            (DBOrg.org_type_code == DBOrgType.code),
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

# Results format: category, subcategory, location_name, location_code, admin1_name, admin1_code, admin2_name, admin2_code, hapi_updated_date
availability_stmt_operational_presence = (
    select(
        literal("coordination-context").label("category"),
        literal("operational-presence").label("subcategory"),
        DBLocation.name.label("location_name"),
        DBLocation.code.label("location_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.code.label("admin2_code"),
        case(
            (
                or_(
                    and_(DBOperationalPresence.provider_admin2_name.is_not(None), DBOperationalPresence.provider_admin2_name != ""),
                    DBAdmin2.is_unspecified.is_(False),
                ),
                2,
            ),
            (
                or_(
                    and_(DBOperationalPresence.provider_admin1_name.is_not(None), DBOperationalPresence.provider_admin1_name != ""),
                    DBAdmin1.is_unspecified.is_(False),
                ),
                1,
            ),
            else_=0,
        ).label("admin_level"),
        DBResource.hapi_updated_date,
    )
    .select_from(
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
        .join(
            DBResource.__table__,
            DBOperationalPresence.resource_hdx_id == DBResource.hdx_id,
        )
    )
    .distinct()
)
