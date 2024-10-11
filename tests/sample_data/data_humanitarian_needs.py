from datetime import datetime

data_humanitarian_needs = [
    # total national
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        provider_admin1_name="Provincia 01",
        provider_admin2_name="Distrito B",
        sector_code="intersectoral",
        category="",
        population_status="AFF",
        population=1_000_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
    # national f, all ages, disabled, sector SHL
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        provider_admin1_name="Provincia 01",
        provider_admin2_name="Distrito B",
        sector_code="SHL",
        category="Female - Refugees",
        population_status="INN",
        population=500_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
    # admin1 f, age 0-4, not disabled, sector WSH
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=2,
        provider_admin1_name="Provincia 01",
        provider_admin2_name="Distrito B",
        sector_code="WSH",
        category="Female - Disabled - Baby - IDP",
        population_status="INN",
        population=5_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
    # admin2 ages 80+, disabled, sector HEA
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=4,
        provider_admin1_name="Provincia 03",
        provider_admin2_name="Distrito D",
        sector_code="HEA",
        category="Elderly - Disabled - IDP",
        population_status="AFF",
        population=500,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
]
