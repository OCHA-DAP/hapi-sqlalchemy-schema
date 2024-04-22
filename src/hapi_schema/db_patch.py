"""Patch table"""

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base


class StateEnum(str, enum.Enum):
    discovered = 1
    executed = 2
    failed = 3
    canceled = 4


class DBPatch(Base):
    __tablename__ = "patch"
    # __table_args__ = (
    #     Index(None, "patch_sequence_number"),
    #     Index(None, "state"),
    # )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    patch_sequence_number: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    commit_hash: Mapped[str] = mapped_column(
        String(48), unique=True, nullable=False
    )
    commit_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    patch_path: Mapped[str] = mapped_column(String(128), nullable=False)
    permanent_download_url: Mapped[str] = mapped_column(
        String(1024), nullable=False, unique=True
    )
    state: Mapped[StateEnum] = mapped_column(
        Enum(StateEnum), nullable=False, index=True
    )
    # discovered -> it was found in the patch repo
    # executed -> the patch was executed successfully
    # failed -> HWA tried to execute the patch but it failed (either pre-conditions
    #     were not met OR the transaction failed and was rolled back)
    # canceled -> it was marked as canceled in the patch repo
