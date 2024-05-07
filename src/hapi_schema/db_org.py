"""Org table and view."""

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_org_type import DBOrgType
from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBOrg(Base):
    __tablename__ = "org"
    __table_args__ = (
        CheckConstraint(
            "(reference_period_end >= reference_period_start) OR (reference_period_start IS NULL)",
            name="reference_period",
        ),
        CheckConstraint(
            "(hapi_replaced_date IS NULL) OR (hapi_replaced_date >= hapi_updated_date)",
            name="hapi_dates",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    acronym = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    org_type_code: Mapped[str] = mapped_column(
        ForeignKey("org_type.code", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
    )
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )
    hapi_updated_date = mapped_column(DateTime, nullable=False, index=True)
    hapi_replaced_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )

    org_type = relationship("DBOrgType")


view_params_org = ViewParams(
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


class DBorg_vat(Base):
    __tablename__ = "org_vat"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    acronym: Mapped[str] = mapped_column(String(32), index=True)
    name: Mapped[str] = mapped_column(String(512))
    org_type_code: Mapped[str] = mapped_column(String(32))
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    hapi_updated_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    hapi_replaced_date: Mapped[datetime] = mapped_column(DateTime, index=True)
    org_type_description: Mapped[str] = mapped_column(String(512), index=True)
