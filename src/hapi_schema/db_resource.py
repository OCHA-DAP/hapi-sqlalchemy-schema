"""Resource table and view."""

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_dataset import DBDataset
from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBResource(Base):
    __tablename__ = "resource"

    hdx_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    dataset_hdx_id: Mapped[str] = mapped_column(
        ForeignKey("dataset.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    format: Mapped[str] = mapped_column(String(32), nullable=False)
    update_date = mapped_column(DateTime, nullable=False)
    is_hxl: Mapped[bool] = mapped_column(Boolean, nullable=False)
    download_url: Mapped[str] = mapped_column(
        String(1024), nullable=False, unique=True
    )
    hapi_updated_date = mapped_column(DateTime, nullable=False)
    dataset = relationship("DBDataset")


view_params_resource = ViewParams(
    name="resource_view",
    metadata=Base.metadata,
    selectable=select(
        *DBResource.__table__.columns,
        DBDataset.hdx_stub.label("dataset_hdx_stub"),
        DBDataset.title.label("dataset_title"),
        DBDataset.hdx_provider_stub.label("dataset_hdx_provider_stub"),
        DBDataset.hdx_provider_name.label("dataset_hdx_provider_name"),
    ).select_from(
        DBResource.__table__.join(
            DBDataset.__table__,
            DBResource.dataset_hdx_id == DBDataset.hdx_id,
            isouter=True,
        )
    ),
)
