"""OperationalPresence table and view."""

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, select
from sqlalchemy.orm import Mapped, aliased, mapped_column, relationship

from hapi_schema.db_location import DBLocation
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    max_age_constraint,
    min_age_constraint,
    population_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.enums import Gender, PopulationGroup
from hapi_schema.utils.view_params import ViewParams


class DBRefugees(Base):
    __tablename__ = "refugees"
    __table_args__ = (
        min_age_constraint(),
        max_age_constraint(),
        population_constraint(),
        reference_period_constraint(),
    )

    resource_hdx_id = mapped_column(
        ForeignKey("resource.hdx_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    origin_location_ref: Mapped[int] = mapped_column(
        ForeignKey("location.id", onupdate="CASCADE"),
        primary_key=True,
    )
    asylum_location_ref: Mapped[int] = mapped_column(
        ForeignKey("location.id", onupdate="CASCADE"),
        primary_key=True,
    )
    population_group: Mapped[PopulationGroup] = mapped_column(
        Enum(PopulationGroup, name="population_group_enum"), primary_key=True
    )
    gender: Mapped[Gender] = mapped_column(
        Enum(Gender, name="gender_enum"), primary_key=True
    )
    age_range: Mapped[str] = mapped_column(String(32), primary_key=True)
    min_age: Mapped[int] = mapped_column(Integer, index=True)
    max_age: Mapped[int] = mapped_column(Integer, index=True)
    population: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )

    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True
    )

    origin_location = relationship(
        "DBLocation",
        foreign_keys=[origin_location_ref],
        primaryjoin="DBRefugees.origin_location_ref == DBLocation.id",
    )

    asylum_location = relationship(
        "DBLocation",
        foreign_keys=[asylum_location_ref],
        primaryjoin="DBRefugees.asylum_location_ref == DBLocation.id",
    )


DBLocationOrigin = aliased(DBLocation)
DBLocationAsylum = aliased(DBLocation)
view_params_operational_presence = ViewParams(
    name="operational_presence_view",
    metadata=Base.metadata,
    selectable=select(
        *DBRefugees.__table__.columns,
        # DBLocationOrigin.code.label("origin_location_code"),
        # DBLocationOrigin.name.label("origin_location_name"),
        # DBLocationAsylum.code.label("asylum_location_code"),
        # DBLocationAsylum.name.label("asylum_location_name"),
        # ).select_from(
        # Join origin and asylum location refs to location table
        #    DBRefugees.__table__.join(
        #        DBLocationOrigin.__table__,
        #        DBRefugees.origin_location_ref == DBLocationOrigin.id,
        #        isouter=True,
        #   )#.join(
        #   DBLocationAsylum.__table__,
        #   DBRefugees.asylum_location_ref == DBLocationAsylum.id,
        #   isouter=True,
        # )
    ),
)
