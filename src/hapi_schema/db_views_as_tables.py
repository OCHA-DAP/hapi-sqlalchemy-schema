from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from hapi_schema.utils.base import Base
from hapi_schema.utils.enums import (
    CommodityCategory,
    DisabledMarker,
    EventType,
    Gender,
    IPCPhase,
    IPCType,
    PopulationGroup,
    PopulationStatus,
    PriceFlag,
    PriceType,
    RiskClass,
    build_enum_using_values,
)


class DBAdmin1VAT(Base):
    __tablename__ = "admin1_vat"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    location_ref: Mapped[int] = mapped_column(Integer)
    code: Mapped[str] = mapped_column(String(128), index=True)
    name: Mapped[str] = mapped_column(String(512), index=True)
    is_unspecified: Mapped[bool] = mapped_column(Boolean)
    from_cods: Mapped[bool] = mapped_column(Boolean)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=True,
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
    from_cods: Mapped[bool] = mapped_column(Boolean)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        index=True,
    )
    admin1_code: Mapped[str] = mapped_column(String(128))
    admin1_name: Mapped[str] = mapped_column(String(512))
    admin1_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    location_ref: Mapped[int] = mapped_column(Integer)
    location_code: Mapped[str] = mapped_column(String(128), index=True)
    location_name: Mapped[str] = mapped_column(String(512), index=True)


class DBConflictEventVAT(Base):
    __tablename__ = "conflict_event_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin2_ref: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[EventType] = mapped_column(
        build_enum_using_values(EventType), primary_key=True
    )
    events: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    fatalities: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=True,
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


class DBCurrencyVAT(Base):
    __tablename__ = "currency_vat"
    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(512), index=True)


class DBDatasetVAT(Base):
    __tablename__ = "dataset_vat"
    hdx_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    hdx_stub: Mapped[str] = mapped_column(String(128), index=True)
    title: Mapped[str] = mapped_column(String(1024))
    hdx_provider_stub: Mapped[str] = mapped_column(String(128), index=True)
    hdx_provider_name: Mapped[str] = mapped_column(String(512), index=True)


class DBFoodPriceVAT(Base):
    __tablename__ = "food_price_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    market_code: Mapped[str] = mapped_column(String(32), primary_key=True)
    commodity_code: Mapped[str] = mapped_column(String(32), primary_key=True)
    currency_code: Mapped[str] = mapped_column(String(32), index=True)
    unit: Mapped[str] = mapped_column(String(32), primary_key=True)
    price_flag: Mapped[PriceFlag] = mapped_column(
        build_enum_using_values(PriceFlag), primary_key=True
    )
    price_type: Mapped[PriceType] = mapped_column(
        build_enum_using_values(PriceType), primary_key=True
    )
    price: Mapped[Decimal] = mapped_column()
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=True,
    )
    admin2_ref: Mapped[int] = mapped_column(Integer)
    market_name: Mapped[str] = mapped_column(String(512), index=True)
    lat: Mapped[float] = mapped_column(Float, index=True)
    lon: Mapped[float] = mapped_column(Float, index=True)
    commodity_category: Mapped[CommodityCategory] = mapped_column(
        build_enum_using_values(CommodityCategory)
    )
    commodity_name: Mapped[str] = mapped_column(String(512), index=True)
    location_code: Mapped[str] = mapped_column(String(128), index=True)
    location_name: Mapped[str] = mapped_column(String(512), index=True)
    location_ref: Mapped[int] = mapped_column(Integer)
    admin1_code: Mapped[str] = mapped_column(String(128), index=True)
    admin1_name: Mapped[str] = mapped_column(String(512), index=True)
    admin1_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    admin1_ref: Mapped[int] = mapped_column(Integer)
    admin2_code: Mapped[str] = mapped_column(String(128), index=True)
    admin2_name: Mapped[str] = mapped_column(String(512), index=True)
    admin2_is_unspecified: Mapped[bool] = mapped_column(Boolean)


class DBFoodSecurityVAT(Base):
    __tablename__ = "food_security_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin2_ref: Mapped[int] = mapped_column(Integer, primary_key=True)
    ipc_phase: Mapped[IPCPhase] = mapped_column(
        build_enum_using_values(IPCPhase), primary_key=True
    )
    ipc_type: Mapped[IPCType] = mapped_column(
        build_enum_using_values(IPCType), primary_key=True
    )
    population_in_phase: Mapped[int] = mapped_column(Integer, index=True)
    population_fraction_in_phase: Mapped[Decimal] = mapped_column(index=True)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=True,
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
    requirements_usd: Mapped[Decimal] = mapped_column(index=True)
    funding_usd: Mapped[Decimal] = mapped_column(index=True)
    funding_pct: Mapped[Decimal] = mapped_column(index=True)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )
    location_code: Mapped[str] = mapped_column(String(128), index=True)
    location_name: Mapped[str] = mapped_column(String(512), index=True)


class DBHumanitarianNeedsVAT(Base):
    __tablename__ = "humanitarian_needs_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin2_ref: Mapped[int] = mapped_column(Integer, primary_key=True)
    gender: Mapped[Gender] = mapped_column(
        build_enum_using_values(Gender), primary_key=True
    )
    age_range: Mapped[str] = mapped_column(String(32), primary_key=True)
    min_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    max_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    sector_code: Mapped[str] = mapped_column(String(32), primary_key=True)
    population_group: Mapped[PopulationGroup] = mapped_column(
        build_enum_using_values(PopulationGroup), primary_key=True
    )
    population_status: Mapped[PopulationStatus] = mapped_column(
        build_enum_using_values(PopulationStatus), primary_key=True
    )
    disabled_marker: Mapped[DisabledMarker] = mapped_column(
        build_enum_using_values(DisabledMarker), primary_key=True
    )
    population: Mapped[int] = mapped_column(Integer)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=True,
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
    from_cods: Mapped[bool] = mapped_column(Boolean)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=True,
    )


class DBNationalRiskVAT(Base):
    __tablename__ = "national_risk_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    location_ref: Mapped[int] = mapped_column(Integer, primary_key=True)
    risk_class: Mapped[RiskClass] = mapped_column(
        build_enum_using_values(RiskClass)
    )
    global_rank: Mapped[int] = mapped_column(Integer)
    overall_risk: Mapped[Decimal] = mapped_column()
    hazard_exposure_risk: Mapped[Decimal] = mapped_column()
    vulnerability_risk: Mapped[Decimal] = mapped_column()
    coping_capacity_risk: Mapped[Decimal] = mapped_column()
    meta_missing_indicators_pct: Mapped[Decimal] = mapped_column(nullable=True)
    meta_avg_recentness_years: Mapped[Decimal] = mapped_column(nullable=True)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=True,
    )
    location_code: Mapped[str] = mapped_column(String(128), index=True)
    location_name: Mapped[str] = mapped_column(String(512), index=True)


class DBOperationalPresenceVAT(Base):
    __tablename__ = "operational_presence_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin2_ref: Mapped[int] = mapped_column(Integer, primary_key=True)
    org_acronym: Mapped[str] = mapped_column(String, primary_key=True)
    org_name: Mapped[str] = mapped_column(String, primary_key=True)
    sector_code: Mapped[str] = mapped_column(String(32), primary_key=True)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=True,
    )
    org_type_code: Mapped[str] = mapped_column(String(32))
    org_type_description: Mapped[str] = mapped_column(String(512), index=True)
    sector_name: Mapped[str] = mapped_column(String(512))
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


class DBOrgTypeVAT(Base):
    __tablename__ = "org_type_vat"
    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    description: Mapped[str] = mapped_column(String(512), index=True)


class DBOrgVAT(Base):
    __tablename__ = "org_vat"
    acronym: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(512), primary_key=True)
    org_type_code: Mapped[str] = mapped_column(
        String(32), nullable=True, index=True
    )
    org_type_description: Mapped[str] = mapped_column(String(512), index=True)


class DBPopulationVAT(Base):
    __tablename__ = "population_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin2_ref: Mapped[int] = mapped_column(Integer, primary_key=True)
    gender: Mapped[Gender] = mapped_column(
        build_enum_using_values(Gender), primary_key=True
    )
    age_range: Mapped[str] = mapped_column(String(32), primary_key=True)
    min_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    max_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    population: Mapped[int] = mapped_column(Integer, index=True)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, index=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=True,
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


class DBPovertyRateVAT(Base):
    __tablename__ = "poverty_rate_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    admin1_ref: Mapped[int] = mapped_column(Integer, primary_key=True)
    admin1_name: Mapped[str] = mapped_column(
        String(512), primary_key=True, index=True
    )
    mpi: Mapped[float] = mapped_column(Float)
    headcount_ratio: Mapped[float] = mapped_column(Float)
    intensity_of_deprivation: Mapped[float] = mapped_column(Float)
    vulnerable_to_poverty: Mapped[float] = mapped_column(Float)
    in_severe_poverty: Mapped[float] = mapped_column(Float)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=True,
    )
    location_code: Mapped[str] = mapped_column(String(128), index=True)
    location_name: Mapped[str] = mapped_column(String(512), index=True)
    admin1_code: Mapped[str] = mapped_column(String(128))
    admin1_is_unspecified: Mapped[bool] = mapped_column(Boolean)
    location_ref: Mapped[int] = mapped_column(Integer, index=True)


class DBRefugeesVAT(Base):
    __tablename__ = "refugees_vat"
    resource_hdx_id: Mapped[str] = mapped_column(String(36))
    origin_location_ref: Mapped[int] = mapped_column(Integer, primary_key=True)
    asylum_location_ref: Mapped[int] = mapped_column(Integer, primary_key=True)
    population_group: Mapped[PopulationGroup] = mapped_column(
        build_enum_using_values(PopulationGroup), primary_key=True
    )
    gender: Mapped[Gender] = mapped_column(
        build_enum_using_values(Gender), primary_key=True
    )
    age_range: Mapped[str] = mapped_column(String(32), primary_key=True)
    min_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    max_age: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    population: Mapped[int] = mapped_column(Integer, index=True)
    reference_period_start: Mapped[datetime] = mapped_column(
        DateTime, primary_key=True
    )
    reference_period_end: Mapped[datetime] = mapped_column(
        DateTime,
        index=True,
        nullable=True,
    )
    origin_location_code: Mapped[str] = mapped_column(String(128), index=True)
    origin_location_name: Mapped[str] = mapped_column(String(512), index=True)
    asylum_location_code: Mapped[str] = mapped_column(String(128), index=True)
    asylum_location_name: Mapped[str] = mapped_column(String(512), index=True)


class DBResourceVAT(Base):
    __tablename__ = "resource_vat"
    hdx_id: Mapped[str] = mapped_column(String(36), primary_key=True)
    dataset_hdx_id: Mapped[str] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(256))
    format: Mapped[str] = mapped_column(String(32))
    update_date: Mapped[datetime] = mapped_column(DateTime)
    is_hxl: Mapped[bool] = mapped_column(Boolean)
    download_url: Mapped[str] = mapped_column(String(1024))
    hapi_updated_date: Mapped[datetime] = mapped_column(DateTime)
    dataset_hdx_stub: Mapped[str] = mapped_column(String(128), index=True)
    dataset_title: Mapped[str] = mapped_column(String(1024))
    dataset_hdx_provider_stub: Mapped[str] = mapped_column(
        String(128), index=True
    )
    dataset_hdx_provider_name: Mapped[str] = mapped_column(
        String(512), index=True
    )


class DBSectorVAT(Base):
    __tablename__ = "sector_vat"
    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(512), index=True)


class DBWfpCommodityVAT(Base):
    __tablename__ = "wfp_commodity_vat"
    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    category: Mapped[CommodityCategory] = mapped_column(
        build_enum_using_values(CommodityCategory), index=True
    )
    name: Mapped[str] = mapped_column(String(512), index=True)


class DBWfpMarketVAT(Base):
    __tablename__ = "wfp_market_vat"
    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    admin2_ref: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(512), index=True)
    lat: Mapped[float] = mapped_column(Float, index=True)
    lon: Mapped[float] = mapped_column(Float, index=True)
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
