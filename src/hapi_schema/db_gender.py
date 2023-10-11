"""Gender table and view."""

from hdx.database.no_timezone import Base
from hdx.database.views import view
from sqlalchemy import CHAR, String, select
from sqlalchemy.orm import Mapped, mapped_column


class DBGender(Base):
    __tablename__ = "gender"

    code: Mapped[str] = mapped_column(CHAR(1), primary_key=True)
    description: Mapped[str] = mapped_column(String(256), nullable=False)


gender_view = view(
    name="gender_view",
    metadata=Base.metadata,
    selectable=select(*DBGender.__table__.columns),
)
