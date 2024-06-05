"""Patch table"""

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams


class StateEnum(str, enum.Enum):
    discovered = 1  # -> it was found in the patch repo
    executed = 2  # -> the patch was executed successfully
    failed = 3  # -> HWA tried to execute the patch but it failed (either pre-conditions
    #                were not met OR the transaction failed and was rolled back)
    canceled = 4  # -> it was marked as canceled in the patch repo


class DBPatch(Base):
    __tablename__ = "patch"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patch_sequence_number: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    commit_hash: Mapped[str] = mapped_column(
        String(48), unique=False, nullable=False
    )
    commit_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    patch_path: Mapped[str] = mapped_column(
        String(512), nullable=False, index=True
    )
    patch_permalink_url: Mapped[str] = mapped_column(
        String(1024), nullable=False, unique=False
    )
    patch_target: Mapped[str] = mapped_column(String(128), nullable=False)
    patch_hash: Mapped[str] = mapped_column(
        String(48), unique=False, nullable=False
    )
    state: Mapped[StateEnum] = mapped_column(
        Enum(StateEnum), nullable=False, index=True
    )
    execution_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, index=True
    )


view_params_patch = ViewParams(
    name="patch_view",
    metadata=Base.metadata,
    selectable=select(*DBPatch.__table__.columns),
)


class DBPatchVAT(Base):
    __tablename__ = "patch_vat"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patch_sequence_number: Mapped[int] = mapped_column(Integer, index=True)
    commit_hash: Mapped[str] = mapped_column(String(48))
    commit_date: Mapped[datetime] = mapped_column(DateTime)
    patch_path: Mapped[str] = mapped_column(String(512), index=True)
    patch_permalink_url: Mapped[str] = mapped_column(String(1024))
    patch_target: Mapped[str] = mapped_column(String(128))
    patch_hash: Mapped[str] = mapped_column(String(48))
    state: Mapped[str] = mapped_column(String(10), index=True)
    execution_date: Mapped[datetime] = mapped_column(DateTime, index=True)
