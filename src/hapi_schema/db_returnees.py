"""Returnees table and view."""

# Note: this one is a bit tricky, because the view has to join with
# the location table twice

from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    select,
)
from sqlalchemy.orm import Mapped, aliased, mapped_column, relationship
from sqlalchemy.sql.expression import literal

from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    max_age_constraint,
    min_age_constraint,
    population_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.enums import (
    Gender,
    PopulationGroup,
    build_enum_using_values,
)
from hapi_schema.utils.view_params import ViewParams


class DBReturnees(Base):
    __tablename__ = "returnees"
    __table_args__ = (
        min_age_constraint(),
        max_age_constraint(),
        population_constraint(),
        reference_period_constraint(),
    )

    resource_hdx_id: Mapped[str] = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    origin_location_ref: Mapped[int] = mapped_column(
        ForeignKey("location.id", onupdate="CASCADE"), primary_key=True
    )
    asylum_location_ref: Mapped[int] = mapped_column(
        ForeignKey("location.id", onupdate="CASCADE"), primary_key=True
    )
    # population_group is broader than we need, but it will do
    population_group: Mapped[PopulationGroup] = mapped_column(
        build_enum_using_values(PopulationGroup), primary_key=True
    )
    gender: Mapped[Gender] = mapped_column(
        build_enum_using_values(Gender), primary_key=True
    )
    age_range: Mapped[str] = mapped_column(String(32), primary_key=True)
    min_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    max_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    population: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    reference_period_start: Mapped[datetime] = mapped_column(primary_key=True)
    reference_period_end: Mapped[datetime] = mapped_column(
        nullable=False, index=True
    )

    # resource = relationship("DBResource")
    origin_country = relationship(
        "DBLocation", foreign_keys=(origin_location_ref)
    )
    asylum_country = relationship(
        "DBLocation", foreign_keys=(asylum_location_ref)
    )


# Use aliases because we join to DBLocation twice
origin_location = aliased(DBLocation)
asylum_location = aliased(DBLocation)
resource = relationship(DBResource)

view_params_returnees = ViewParams(
    name="returnees_view",
    metadata=Base.metadata,
    selectable=select(
        *DBReturnees.__table__.columns,
        origin_location.code.label("origin_location_code"),
        origin_location.name.label("origin_location_name"),
        origin_location.has_hrp.label("origin_has_hrp"),
        origin_location.in_gho.label("origin_in_gho"),
        asylum_location.code.label("asylum_location_code"),
        asylum_location.name.label("asylum_location_name"),
        asylum_location.has_hrp.label("asylum_has_hrp"),
        asylum_location.in_gho.label("asylum_in_gho"),
    ).select_from(
        # Join pop to admin2 to admin1 to loc
        DBReturnees.__table__.join(
            origin_location,
            DBReturnees.origin_location_ref == origin_location.id,
            isouter=True,
        ).join(
            asylum_location,
            DBReturnees.asylum_location_ref == asylum_location.id,
            isouter=True,
        )
    ),
)

# Results format: category, subcategory, location_name, location_code, admin1_name, admin1_code, admin2_name, admin2_code, hapi_updated_date
availability_stmt_returnees = (
    select(
        literal("affected-people").label("category"),
        literal("returnees").label("subcategory"),
        DBLocation.name.label("location_name"),
        DBLocation.code.label("location_code"),
        literal("").label("admin1_name"),
        literal("").label("admin1_code"),
        literal("").label("admin2_name"),
        literal("").label("admin2_code"),
        literal(0).label("admin_level"),
        DBResource.hapi_updated_date,
    )
    .select_from(
        DBReturnees.__table__.join(
            DBLocation.__table__,
            (DBReturnees.asylum_location_ref == DBLocation.id)
            | (DBReturnees.origin_location_ref == DBLocation.id),
            isouter=True,
        ).join(
            DBResource.__table__,
            DBReturnees.resource_hdx_id == DBResource.hdx_id,
        )
    )
    .distinct()
)
