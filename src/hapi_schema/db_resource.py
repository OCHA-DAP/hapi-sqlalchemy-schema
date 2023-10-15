"""Resource table and view."""

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_dataset import DBDataset
from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBResource(Base):
    __tablename__ = "resource"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dataset_ref: Mapped[int] = mapped_column(
        ForeignKey("dataset.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    hdx_id: Mapped[str] = mapped_column(
        String(36), unique=True, nullable=False
    )
    filename: Mapped[str] = mapped_column(String(256), nullable=False)
    format: Mapped[str] = mapped_column(String(32), nullable=False)
    update_date = mapped_column(DateTime, nullable=False, index=True)
    download_url: Mapped[str] = mapped_column(
        String(1024), nullable=False, unique=True
    )
    is_hxl: Mapped[bool] = mapped_column(Boolean, nullable=False, index=True)

    dataset = relationship("DBDataset")


view_params_resource = ViewParams(
    name="resource_view",
    metadata=Base.metadata,
    selectable=select(
        *DBResource.__table__.columns,
        DBDataset.hdx_id.label("dataset_hdx_id"),
        DBDataset.hdx_stub.label("dataset_hdx_stub"),
        DBDataset.title.label("dataset_title"),
        DBDataset.provider_code.label("dataset_provider_code"),
        DBDataset.provider_name.label("dataset_provider_name"),
    ).select_from(
        DBResource.__table__.join(
            DBDataset.__table__,
            DBResource.dataset_ref == DBDataset.id,
            isouter=True,
        )
    ),
)
