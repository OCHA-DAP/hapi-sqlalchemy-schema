"""FoodPrice table and view."""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    ForeignKey,
    String,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_admin2 import DBAdmin1, DBAdmin2, DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    reference_period_constraint,
)
from hapi_schema.utils.enums import PriceFlag, PriceType
from hapi_schema.utils.view_params import ViewParams


# normalised table
class DBFoodPrice(Base):
    __tablename__ = "food_price"
    __table_args__ = (reference_period_constraint(),)

    resource_hdx_id: Mapped[str] = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"),
        primary_key=True,
    )
    commodity_code: Mapped[str] = mapped_column(
        ForeignKey("wfp_commodity.code"), primary_key=True
    )
    currency_code: Mapped[str] = mapped_column(
        ForeignKey("currency.code", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    price_flag: Mapped[PriceFlag] = mapped_column(
        Enum(PriceFlag), nullable=False, primary_key=True
    )
    price_type: Mapped[PriceType] = mapped_column(
        Enum(PriceType), nullable=False, primary_key=True
    )
    price: Mapped[float] = mapped_column(Float, nullable=False)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True
    )

    resource = relationship(DBResource)
    admin2 = relationship(DBAdmin2)


# view
view_params_food_price = ViewParams(
    name="food_price_view",
    metadata=Base.metadata,
    selectable=select(
        *DBFoodPrice.__table__.columns,
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin1.location_ref.label("location_ref"),
        DBAdmin2.code.label("admin2_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.is_unspecified.label("admin2_is_unspecified"),
        DBAdmin2.admin1_ref.label("admin1_ref"),
    ).select_from(
        # Join risk to admin2
        DBFoodPrice.__table__.join(
            DBAdmin2.__table__,
            DBFoodPrice.admin2_ref == DBAdmin2.id,
            isouter=True,
        )
        .join(
            DBAdmin1.__table__,
            DBAdmin2.admin1_ref == DBAdmin1.id,
            isouter=True,
        )
        .join(
            DBLocation.__table__,
            DBAdmin1.location_ref == DBLocation.id,
            isouter=True,
        )
    ),
)
