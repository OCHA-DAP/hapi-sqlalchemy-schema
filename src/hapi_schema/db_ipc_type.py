"""IPC type table and view."""

from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBIpcType(Base):
    __tablename__ = "ipc_type"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    description: Mapped[str] = mapped_column(String(512), nullable=False)


view_params_ipc_type = ViewParams(
    name="ipca_type_vew",
    metadata=Base.metadata,
    selectable=select(*DBIpcType.__table__.columns),
)
