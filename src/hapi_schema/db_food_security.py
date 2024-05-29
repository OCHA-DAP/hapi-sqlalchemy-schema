"""Food security table and view."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True
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
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin1.location_ref.label("location_ref"),
        DBAdmin2.code.label("admin2_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.is_unspecified.label("admin2_is_unspecified"),
        DBAdmin2.admin1_ref.label("admin1_ref"),
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
