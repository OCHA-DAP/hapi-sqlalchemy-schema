"""Population table and view."""

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
    select,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_dataset import DBDataset
from hapi_schema.db_ipc_phase import DBIpcPhase
from hapi_schema.db_ipc_type import DBIpcType
from hapi_schema.db_location import DBLocation
from hapi_schema.db_resource import DBResource
from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class DBFoodSecurity(Base):
    __tablename__ = "food_security"
    __table_args__ = (
        CheckConstraint(
            "population_fraction_in_phase >= 0 AND population_fraction_in_phase <=1",
            name="population_fraction_in_phase",
        ),
        CheckConstraint(
            "(reference_period_end >= reference_period_start) OR (reference_period_start IS NULL)",
            name="reference_period",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    resource_ref: Mapped[int] = mapped_column(
        ForeignKey("resource.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    admin2_ref: Mapped[int] = mapped_column(
        ForeignKey("admin2.id", onupdate="CASCADE"), nullable=False
    )
    ipc_phase_code: Mapped[str] = mapped_column(
        ForeignKey("ipc_phase.code", onupdate="CASCADE"), nullable=False
    )
    ipc_type_code: Mapped[str] = mapped_column(
        ForeignKey("ipc_type.code", onupdate="CASCADE"), nullable=False
    )
    population_in_phase: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    population_fraction_in_phase: Mapped[float] = mapped_column(
        Float, nullable=False, index=True
    )
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, server_default=text("NULL"), index=True
    )
    source_data: Mapped[str] = mapped_column(Text, nullable=True)

    resource = relationship("DBResource")
    admin2 = relationship("DBAdmin2")
    ipc_phase = relationship("DBIpcPhase")
    ipc_type = relationship("DBIpcType")


view_params_food_security = ViewParams(
    name="food_security_view",
    metadata=Base.metadata,
    selectable=select(
        *DBFoodSecurity.__table__.columns,
        DBDataset.hdx_id.label("dataset_hdx_id"),
        DBDataset.hdx_stub.label("dataset_hdx_stub"),
        DBDataset.title.label("dataset_title"),
        DBDataset.hdx_provider_stub.label("dataset_hdx_provider_stub"),
        DBDataset.hdx_provider_name.label("dataset_hdx_provider_name"),
        DBIpcPhase.name.label("ipc_phase_name"),
        DBResource.hdx_id.label("resource_hdx_id"),
        DBResource.name.label("resource_name"),
        DBResource.update_date.label("resource_update_date"),
        DBLocation.code.label("location_code"),
        DBLocation.name.label("location_name"),
        DBAdmin1.code.label("admin1_code"),
        DBAdmin1.name.label("admin1_name"),
        DBAdmin1.is_unspecified.label("admin1_is_unspecified"),
        DBAdmin2.code.label("admin2_code"),
        DBAdmin2.name.label("admin2_name"),
        DBAdmin2.is_unspecified.label("admin2_is_unspecified"),
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
        # Join pop to resource to dataset
        .join(
            DBResource.__table__,
            DBFoodSecurity.resource_ref == DBResource.id,
            isouter=True,
        )
        .join(
            DBDataset.__table__,
            DBResource.dataset_ref == DBDataset.id,
            isouter=True,
        )
        # Join to ipc phase
        .join(
            DBIpcPhase.__table__,
            DBFoodSecurity.ipc_phase_code == DBIpcPhase.code,
            isouter=True,
        )
        # Join to ipc type
        .join(
            DBIpcType.__table__,
            DBFoodSecurity.ipc_type_code == DBIpcType.code,
            isouter=True,
        )
    ),
)
