"""HumanitarianNeeds table and view."""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_location import DBLocation
from hapi_schema.db_sector import DBSector
from hapi_schema.utils.base import Base
from hapi_schema.utils.constraints import (
    max_age_constraint,
    min_age_constraint,
    population_constraint,
    reference_period_constraint,
)
from hapi_schema.utils.enums import (
    DisabledMarker,
    Gender,
    PopulationGroup,
    PopulationStatus,
    build_enum_using_values,
)
from hapi_schema.utils.view_params import ViewParams


class DBHumanitarianNeeds(Base):
    __tablename__ = "humanitarian_needs"
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
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"),
        primary_key=True,
    )
    gender: Mapped[Gender] = mapped_column(
        build_enum_using_values(Gender), primary_key=True
    )
    age_range: Mapped[str] = mapped_column(String(32), primary_key=True)
    min_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    max_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    sector_code: Mapped[str] = mapped_column(
        ForeignKey("sector.code", onupdate="CASCADE"),
        primary_key=True,
    )
    population_group: Mapped[PopulationGroup] = mapped_column(
        build_enum_using_values(PopulationGroup),
        primary_key=True,
    )

    population_status: Mapped[PopulationStatus] = mapped_column(
        build_enum_using_values(PopulationStatus),
        primary_key=True,
    )

    disabled_marker: Mapped[DisabledMarker] = mapped_column(
        build_enum_using_values(DisabledMarker), primary_key=True
    )
    population: Mapped[int] = mapped_column(Integer, nullable=False)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime,
        primary_key=True,
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True
    )

    resource = relationship("DBResource")
    admin2 = relationship("DBAdmin2")
    sector = relationship("DBSector")


view_params_humanitarian_needs = ViewParams(
    name="humanitarian_needs_view",
    metadata=Base.metadata,
    selectable=select(
        *DBHumanitarianNeeds.__table__.columns,
        DBSector.name.label("sector_name"),
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBAdmin1.location_ref.label("location_ref"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin2.code.label("admin2_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.is_unspecified.label("admin2_is_unspecified"),
        DBAdmin2.admin1_ref.label("admin1_ref"),
    ).select_from(
        # Join pop to admin2 to admin1 to loc
        DBHumanitarianNeeds.__table__.join(
            DBAdmin2.__table__,
            DBHumanitarianNeeds.admin2_ref == DBAdmin2.id,
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
        # Join needs to sector
        .join(
            DBSector.__table__,
            DBHumanitarianNeeds.sector_code == DBSector.code,
            isouter=True,
        )
    ),
)
