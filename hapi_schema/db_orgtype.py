"""OrgType table."""

from hdx.database.no_timezone import Base
from sqlalchemy import select, String
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.view import view


class DBOrgType(Base):
    __tablename__ = "org_type"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    description: Mapped[str] = mapped_column(String(512), nullable=False)


org_type_view = view(
    name="org_type_view",
    metadata=Base.metadata,
    selectable=select(*DBOrgType.__table__.columns),
)