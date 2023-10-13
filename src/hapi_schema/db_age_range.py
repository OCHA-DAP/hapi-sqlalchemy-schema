"""Age range table and view."""

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBAgeRange(Base):
    __tablename__ = "age_range"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    age_min: Mapped[int] = mapped_column(Integer, nullable=False)
    age_max: Mapped[int] = mapped_column(Integer, nullable=True)


age_range_view_params = ViewParams(
    name="age_range_view",
    metadata=Base.metadata,
    selectable=select(*DBAgeRange.__table__.columns),
)
