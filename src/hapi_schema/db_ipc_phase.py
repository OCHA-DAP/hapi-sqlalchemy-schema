"""IPC phase table and view."""

from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBIpcPhase(Base):
    __tablename__ = "ipc_phase"

    code: Mapped[int] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False)


view_params_ipc_phase = ViewParams(
    name="ipc_phase_view",
    metadata=Base.metadata,
    selectable=select(*DBIpcPhase.__table__.columns),
)
