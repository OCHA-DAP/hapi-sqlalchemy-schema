from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base


class DBAdmin1VAT(Base):
    __tablename__ = "admin1_vat"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    location_ref: Mapped[int] = mapped_column(Integer)
    code: Mapped[str] = mapped_column(String(128), index=True)
    name: Mapped[str] = mapped_column(String(512), index=True)
    is_unspecified: Mapped[bool] = mapped_column(Boolean)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    location_code: Mapped[str] = mapped_column(String(128), index=True)
    location_name: Mapped[str] = mapped_column(String(512), index=True)


class DBAdmin2VAT(Base):
    __tablename__ = "admin2_vat"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    admin1_ref: Mapped[int] = mapped_column(Integer)
    code: Mapped[str] = mapped_column(String(128), index=True)
    name: Mapped[str] = mapped_column(String(512), index=True)
    is_unspecified: Mapped[bool] = mapped_column(Boolean)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, index=True
    )
    admin1_code: Mapped[str] = mapped_column(String(128))
    admin1_name: Mapped[str] = mapped_column(String(512))
    admin1_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    location_code: Mapped[str] = mapped_column(String(128), index=True)
    location_name: Mapped[str] = mapped_column(String(512), index=True)


class DBDatasetVAT(Base):
    __tablename__ = "dataset_vat"
    hdx_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    hdx_stub: Mapped[str] = mapped_column(String(128), index=True)
    title: Mapped[str] = mapped_column(String(1024))
    hdx_provider_stub: Mapped[str] = mapped_column(String(128), index=True)
    hdx_provider_name: Mapped[str] = mapped_column(String(512), index=True)


class DBFoodSecurityVAT(Base):
    __tablename__ = "food_security_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin2_ref: Mapped[int] = mapped_column(Integer, primary_key=True)
    ipc_phase: Mapped[str] = mapped_column(String(12), primary_key=True)
    ipc_type: Mapped[str] = mapped_column(String(17), primary_key=True)
    population_in_phase: Mapped[int] = mapped_column(Integer, index=True)
    population_fraction_in_phase: Mapped[float] = mapped_column(
        Float, index=True
    )
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    location_code: Mapped[str] = mapped_column(String(128), index=True)
    location_name: Mapped[str] = mapped_column(String(512), index=True)
    admin1_code: Mapped[str] = mapped_column(String(128), index=True)
    admin1_name: Mapped[str] = mapped_column(String(512), index=True)
    admin1_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    location_ref: Mapped[int] = mapped_column(Integer)
    admin2_code: Mapped[str] = mapped_column(String(128), index=True)
    admin2_name: Mapped[str] = mapped_column(String(512), index=True)
    admin2_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    admin1_ref: Mapped[int] = mapped_column(Integer)


class DBFundingVAT(Base):
    __tablename__ = "funding_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    appeal_code: Mapped[str] = mapped_column(String(32), primary_key=True)
    location_ref: Mapped[int] = mapped_column(Integer, primary_key=True)
    appeal_name: Mapped[str] = mapped_column(String(256))
    appeal_type: Mapped[str] = mapped_column(String(32))
    requirements_usd: Mapped[float] = mapped_column(Float, index=True)
    funding_usd: Mapped[float] = mapped_column(Float, index=True)
    funding_pct: Mapped[float] = mapped_column(Float, index=True)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, nullable=True
    )
    location_code: Mapped[str] = mapped_column(String(128), index=True)
    location_name: Mapped[str] = mapped_column(String(512), index=True)


class DBHumanitarianNeedsVAT(Base):
    __tablename__ = "humanitarian_needs_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin2_ref: Mapped[int] = mapped_column(Integer, primary_key=True)
    gender: Mapped[str] = mapped_column(String(11), primary_key=True)
    age_range: Mapped[str] = mapped_column(String(32), primary_key=True)
    min_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    max_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    sector_code: Mapped[str] = mapped_column(String(32))
    population_group: Mapped[str] = mapped_column(String(14), primary_key=True)
    population_status: Mapped[str] = mapped_column(
        String(10), primary_key=True
    )
    disabled_marker: Mapped[str] = mapped_column(String(3), primary_key=True)
    population: Mapped[int] = mapped_column(Integer, primary_key=True)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    sector_name: Mapped[str] = mapped_column(String(512))
    location_code: Mapped[str] = mapped_column(String(128), index=True)
    location_name: Mapped[str] = mapped_column(String(512), index=True)
    location_ref: Mapped[int] = mapped_column(Integer)
    admin1_code: Mapped[str] = mapped_column(String(128), index=True)
    admin1_name: Mapped[str] = mapped_column(String(512), index=True)
    admin1_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    admin2_code: Mapped[str] = mapped_column(String(128), index=True)
    admin2_name: Mapped[str] = mapped_column(String(512), index=True)
    admin2_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    admin1_ref: Mapped[int] = mapped_column(Integer)


class DBLocationVAT(Base):
    __tablename__ = "location_vat"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(128), index=True)
    name: Mapped[str] = mapped_column(String(512), index=True)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
