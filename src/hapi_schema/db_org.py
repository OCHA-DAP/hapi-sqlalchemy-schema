"""Org table."""
from datetime import datetime

from hdx.database.no_timezone import Base
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_orgtype import DBOrgType  # noqa: F401


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
