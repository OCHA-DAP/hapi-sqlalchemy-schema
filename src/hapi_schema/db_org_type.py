"""OrgType table and view."""

from hdx.database.views import view
from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.base import Base


class DBOrgType(Base):
    __tablename__ = "org_type"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    description: Mapped[str] = mapped_column(String(512), nullable=False)


org_type_view = view(
    name="org_type_view",
    metadata=Base.metadata,
    selectable=select(*DBOrgType.__table__.columns),
)
