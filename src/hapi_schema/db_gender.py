"""Gender table and view."""

from sqlalchemy import CHAR, String, select
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBGender(Base):
    __tablename__ = "gender"

    code: Mapped[str] = mapped_column(CHAR(1), primary_key=True)
    description: Mapped[str] = mapped_column(String(256), nullable=False)


gender_view_params = ViewParams(
    name="gender_view",
    metadata=Base.metadata,
    selectable=select(*DBGender.__table__.columns),
)
