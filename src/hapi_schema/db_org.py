"""Org table and view."""
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.base import Base
from hapi_schema.db_org_type import DBOrgType
from hapi_schema.view_params import ViewParams


class DBOrg(Base):
    __tablename__ = "org"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    acronym = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    org_type_code: Mapped[str] = mapped_column(
        ForeignKey("org_type.code", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
    )
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL")
    )

    org_type = relationship("DBOrgType")


org_view_params = ViewParams(
    name="org_view",
    metadata=Base.metadata,
    selectable=select(
        *DBOrg.__table__.columns,
        DBOrgType.description.label("org_type_description"),
    ).select_from(
        DBOrg.__table__.join(
            DBOrgType.__table__,
            DBOrg.org_type_code == DBOrgType.code,
            isouter=True,
        )
    ),
)
