"""Food security table and view."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Float,
    ForeignKey,
    Integer,
    String,
    case,
    or_,
    select, and_,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import literal

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    population_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.enums import IPCPhase, IPCType, build_enum_using_values
from hapi_schema.utils.view_params import ViewParams


class DBFoodSecurity(Base):
    __tablename__ = "food_security"
    __table_args__ = (
        reference_period_constraint(),
        population_constraint(population_var_name="population_in_phase"),
    )

    resource_hdx_id: Mapped[str] = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"), primary_key=True
    )
    provider_admin1_name = mapped_column(String(512), primary_key=True)
    provider_admin2_name = mapped_column(String(512), primary_key=True)
    ipc_phase: Mapped[IPCPhase] = mapped_column(
        build_enum_using_values(IPCPhase), primary_key=True
    )
    ipc_type: Mapped[IPCType] = mapped_column(
        build_enum_using_values(IPCType), primary_key=True
    )
    population_in_phase: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    population_fraction_in_phase: Mapped[Decimal] = mapped_column(
        Float, nullable=False, index=True
    )
    reference_period_start: Mapped[datetime] = mapped_column(primary_key=True)
    reference_period_end: Mapped[datetime] = mapped_column(
        nullable=False, index=True
    )

    resource = relationship(DBResource)
    admin2 = relationship(DBAdmin2)


view_params_food_security = ViewParams(
    name="food_security_view",
    metadata=Base.metadata,
    selectable=select(
        *DBFoodSecurity.__table__.columns,
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBLocation.has_hrp.label("has_hrp"),
        DBLocation.in_gho.label("in_gho"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin1.location_ref.label("location_ref"),
        DBAdmin2.code.label("admin2_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.is_unspecified.label("admin2_is_unspecified"),
        DBAdmin2.admin1_ref.label("admin1_ref"),
        case(
            (
                or_(
                    and_(DBFoodSecurity.provider_admin2_name.is_not(None), DBFoodSecurity.provider_admin2_name != ""),
                    DBAdmin2.is_unspecified.is_(False),
                ),
                2,
            ),
            (
                or_(
                    and_(DBFoodSecurity.provider_admin1_name.is_not(None), DBFoodSecurity.provider_admin1_name != ""),
                    DBAdmin1.is_unspecified.is_(False),
                ),
                1,
            ),
            else_=0,
        ).label("admin_level"),
    ).select_from(
        # Join pop to admin2 to admin1 to loc
        DBFoodSecurity.__table__.join(
            DBAdmin2.__table__,
            DBFoodSecurity.admin2_ref == DBAdmin2.id,
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


# Results format: category, subcategory, location_name, location_code, admin1_name, admin1_code, admin2_name, admin2_code, hapi_updated_date
availability_stmt_food_security = (
    select(
        literal("food").label("category"),
        literal("food-security").label("subcategory"),
        DBLocation.name.label("location_name"),
        DBLocation.code.label("location_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.code.label("admin2_code"),
        case(
            (
                or_(
                    and_(DBFoodSecurity.provider_admin2_name.is_not(None), DBFoodSecurity.provider_admin2_name != ""),
                    DBAdmin2.is_unspecified.is_(False),
                ),
                2,
            ),
            (
                or_(
                    and_(DBFoodSecurity.provider_admin1_name.is_not(None), DBFoodSecurity.provider_admin1_name != ""),
                    DBAdmin1.is_unspecified.is_(False),
                ),
                1,
            ),
            else_=0,
        ).label("admin_level"),
        DBResource.hapi_updated_date,
    )
    .select_from(
        DBFoodSecurity.__table__.join(
            DBAdmin2.__table__,
            DBFoodSecurity.admin2_ref == DBAdmin2.id,
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
            DBFoodSecurity.resource_hdx_id == DBResource.hdx_id,
        )
    )
    .distinct()
)
