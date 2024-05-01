from datetime import datetime

data_humanitarian_needs = [
    # total national
    dict(
        id=1,
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        gender_code=None,
        min_age=None,
        max_age=None,
        disabled_marker=None,
        sector_code=None,
        population_group_code=None,
        population_status_code="affected",
        population=1_000_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
    # national f, all ages, disabled, sector SHL
    dict(
        id=2,
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        gender_code="f",
        min_age=None,
        max_age=None,
        disabled_marker=True,
        sector_code="SHL",
        population_group_code="refugees",
        population_status_code="inneed",
        population=500_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
    # admin1 f, age 0-4, not disabled, sector WSH
    dict(
        id=3,
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=2,
        gender_code="f",
        min_age=None,
        max_age=4,
        disabled_marker=True,
        sector_code="WSH",
        population_group_code="idps",
        population_status_code="inneed",
        population=5_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
    # admin2 ages 80+, disabled, sector HEA
    dict(
        id=4,
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=4,
        gender_code=None,
        min_age=80,
        max_age=None,
        disabled_marker=False,
        sector_code="HEA",
        population_group_code="idps",
        population_status_code="affected",
        population=500,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
]
