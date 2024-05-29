"""wfp_commodity table and view."""

from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base
from hapi_schema.utils.enums import CommodityCategory, build_enum_using_values
from hapi_schema.utils.view_params import ViewParams


class DBWFPCommodity(Base):
    __tablename__ = "wfp_commodity"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    category: Mapped[CommodityCategory] = mapped_column(
        build_enum_using_values(CommodityCategory), index=True
    )
    name: Mapped[str] = mapped_column(String(512), nullable=False, index=True)


view_params_wfp_commodity = ViewParams(
    name="wfp_commodity_view",
    metadata=Base.metadata,
    selectable=select(*DBWFPCommodity.__table__.columns),
)
