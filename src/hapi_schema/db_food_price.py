"""FoodPrice table and view."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    String,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import literal

from hapi_schema.db_admin2 import DBAdmin1, DBAdmin2, DBLocation
from hapi_schema.db_currency import DBCurrency
from hapi_schema.db_resource import DBResource
from hapi_schema.db_wfp_commodity import DBWFPCommodity
from hapi_schema.db_wfp_market import DBWFPMarket
from hapi_schema.utils import endpoint_constants
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    non_negative_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.enums import (
    PriceFlag,
    PriceType,
    build_enum_using_values,
)
from hapi_schema.utils.view_params import ViewParams
from hapi_schema.views import get_admin2_case

# normalised table


class DBFoodPrice(Base):
    __tablename__ = "food_price"
    __table_args__ = (
        non_negative_constraint(var_name="price"),
        reference_period_constraint(),
    )

    resource_hdx_id: Mapped[str] = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    market_code: Mapped[str] = mapped_column(
        ForeignKey("wfp_market.code"), primary_key=True
    )
    commodity_code: Mapped[str] = mapped_column(
        ForeignKey("wfp_commodity.code"), primary_key=True
    )
    currency_code: Mapped[str] = mapped_column(
        ForeignKey("currency.code", onupdate="CASCADE"),
        nullable=False,
        index=True,
    )
    unit: Mapped[str] = mapped_column(String(32), primary_key=True)
    price_flag: Mapped[PriceFlag] = mapped_column(
        build_enum_using_values(PriceFlag), primary_key=True
    )
    price_type: Mapped[PriceType] = mapped_column(
        build_enum_using_values(PriceType), primary_key=True
    )
    price: Mapped[Decimal] = mapped_column(nullable=False)
    reference_period_start: Mapped[datetime] = mapped_column(primary_key=True)
    reference_period_end: Mapped[datetime] = mapped_column(
        nullable=False, index=True
    )

    resource = relationship(DBResource)
    market = relationship(DBWFPMarket)
    commodity = relationship(DBWFPCommodity)
    currency = relationship(DBCurrency)


# denormalised view


view_params_food_price = ViewParams(
    name="food_price_view",
    metadata=Base.metadata,
    selectable=select(
        *DBFoodPrice.__table__.columns,
        DBWFPMarket.admin2_ref.label("admin2_ref"),
        DBWFPMarket.provider_admin1_name.label("provider_admin1_name"),
        DBWFPMarket.provider_admin2_name.label("provider_admin2_name"),
        DBWFPMarket.name.label("market_name"),
        DBWFPMarket.lat.label("lat"),
        DBWFPMarket.lon.label("lon"),
        DBWFPCommodity.category.label("commodity_category"),
        DBWFPCommodity.name.label("commodity_name"),
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBLocation.has_hrp.label("has_hrp"),
        DBLocation.in_gho.label("in_gho"),
        DBAdmin1.location_ref.label("location_ref"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin2.admin1_ref.label("admin1_ref"),
        DBAdmin2.code.label("admin2_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.is_unspecified.label("admin2_is_unspecified"),
        get_admin2_case(DBWFPMarket),
    ).select_from(
        # the admin2 comes from wfp_market
        DBFoodPrice.__table__.join(
            DBWFPMarket.__table__,
            DBFoodPrice.market_code == DBWFPMarket.code,
            isouter=True,
        )
        .join(
            DBAdmin2.__table__,
            DBWFPMarket.admin2_ref == DBAdmin2.id,
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
        .join(
            DBWFPCommodity.__table__,
            DBFoodPrice.commodity_code == DBWFPCommodity.code,
            isouter=True,
        )
    ),
)


# Results format: category, subcategory, location_name, location_code, admin1_name, admin1_code, admin2_name, admin2_code, hapi_updated_date
availability_stmt_food_price = (
    select(
        literal(endpoint_constants.FOOD_PRICE_CAT).label("category"),
        literal(endpoint_constants.FOOD_PRICE_SUBCAT).label("subcategory"),
        DBLocation.name.label("location_name"),
        DBLocation.code.label("location_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.code.label("admin2_code"),
        get_admin2_case(DBWFPMarket),
        DBResource.hapi_updated_date,
    )
    .select_from(
        # the admin2 comes from wfp_market
        DBFoodPrice.__table__.join(
            DBWFPMarket.__table__,
            DBFoodPrice.market_code == DBWFPMarket.code,
            isouter=True,
        )
        .join(
            DBAdmin2.__table__,
            DBWFPMarket.admin2_ref == DBAdmin2.id,
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
        .join(
            DBResource.__table__,
            DBFoodPrice.resource_hdx_id == DBResource.hdx_id,
        )
    )
    .distinct()
)
