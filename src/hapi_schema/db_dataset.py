"""Dataset table and view."""

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.base import Base
from hapi_schema.view_params import ViewParams


class DBDataset(Base):
    __tablename__ = "dataset"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hdx_id: Mapped[str] = mapped_column(
        String(36), unique=True, nullable=False
    )
    hdx_stub: Mapped[str] = mapped_column(
        String(128), unique=True, nullable=False
    )
    title = mapped_column(String(1024), nullable=False)
    provider_code: Mapped[str] = mapped_column(
        String(128), nullable=False, index=True
    )
    provider_name: Mapped[str] = mapped_column(
        String(512), nullable=False, index=True
    )


dataset_view_params = ViewParams(
    name="dataset_view",
    metadata=Base.metadata,
    selectable=select(*DBDataset.__table__.columns),
)
