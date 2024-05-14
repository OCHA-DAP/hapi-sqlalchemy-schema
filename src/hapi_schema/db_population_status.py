"""Population status table and view."""

from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBPopulationStatus(Base):
    __tablename__ = "population_status"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    description: Mapped[str] = mapped_column(
        String(512), nullable=False, index=True
    )


view_params_population_status = ViewParams(
    name="population_status_view",
    metadata=Base.metadata,
    selectable=select(*DBPopulationStatus.__table__.columns),
)
