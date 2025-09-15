"""ConflictEvent table and view."""

from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import literal

from hapi_schema.db_admin1 import DBAdmin1, DBLocation
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_resource import DBResource
from hapi_schema.utils import endpoint_constants
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    population_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.enums import EventType, build_enum_using_values
from hapi_schema.utils.view_params import ViewParams
from hapi_schema.views import get_admin2_case


# normalised table
class DBConflictEvent(Base):
    __tablename__ = "conflict_event"
    __table_args__ = (
        population_constraint(population_var_name="events"),  # not really a population
        population_constraint(population_var_name="fatalities"),
        reference_period_constraint(),
    )

    resource_hdx_id: Mapped[str] = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    provider_admin1_name = mapped_column(String(512), primary_key=True)
    provider_admin2_name = mapped_column(String(512), primary_key=True)
    event_type: Mapped[EventType] = mapped_column(
        build_enum_using_values(EventType), nullable=False, primary_key=True
    )
    events: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    fatalities: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    reference_period_start: Mapped[datetime] = mapped_column(primary_key=True)
    reference_period_end: Mapped[datetime] = mapped_column(nullable=False, index=True)

    resource = relationship(DBResource)
    admin2 = relationship(DBAdmin2)


# view
view_params_conflict_event = ViewParams(
    name="conflict_event_view",
    metadata=Base.metadata,
    selectable=select(
        *DBConflictEvent.__table__.columns,
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
        get_admin2_case(DBConflictEvent),
    ).select_from(
        # Join risk to admin2
        DBConflictEvent.__table__.join(
            DBAdmin2.__table__,
            DBConflictEvent.admin2_ref == DBAdmin2.id,
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
availability_stmt_conflict_event = (
    select(
        literal(endpoint_constants.CONFLICT_EVENT_CAT).label("category"),
        literal(endpoint_constants.CONFLICT_EVENT_SUBCAT).label("subcategory"),
        DBLocation.name.label("location_name"),
        DBLocation.code.label("location_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.code.label("admin2_code"),
        get_admin2_case(DBConflictEvent),
        DBResource.hapi_updated_date,
    )
    .select_from(
        DBConflictEvent.__table__.join(
            DBAdmin2.__table__,
            DBConflictEvent.admin2_ref == DBAdmin2.id,
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
            DBConflictEvent.resource_hdx_id == DBResource.hdx_id,
        )
    )
    .distinct()
)
