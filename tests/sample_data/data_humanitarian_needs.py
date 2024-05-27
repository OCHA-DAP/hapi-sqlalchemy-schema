from datetime import datetime

data_humanitarian_needs = [
    # total national
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        gender="all",
        age_range="all",
        disabled_marker="all",
        sector_code="intersectoral",
        population_group="all",
        population_status="AFF",
        population=1_000_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
    # national f, all ages, disabled, sector SHL
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        gender="f",
        age_range="all",
        disabled_marker="n",
        sector_code="SHL",
        population_group="REF",
        population_status="INN",
        population=500_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
    # admin1 f, age 0-4, not disabled, sector WSH
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=2,
        gender="f",
        age_range="0-4",
        min_age=0,
        max_age=4,
        disabled_marker="y",
        sector_code="WSH",
        population_group="IDP",
        population_status="INN",
        population=5_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
    # admin2 ages 80+, disabled, sector HEA
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=4,
        gender="all",
        age_range="80+",
        min_age=80,
        disabled_marker="y",
        sector_code="HEA",
        population_group="IDP",
        population_status="AFF",
        population=500,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
]
