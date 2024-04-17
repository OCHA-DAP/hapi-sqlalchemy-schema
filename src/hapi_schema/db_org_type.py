"""OrgType table and view."""

from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBOrgType(Base):
    __tablename__ = "org_type"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    description: Mapped[str] = mapped_column(
        String(512), nullable=False, index=True
    )


view_params_org_type = ViewParams(
    name="org_type_view",
    metadata=Base.metadata,
    selectable=select(*DBOrgType.__table__.columns),
)
