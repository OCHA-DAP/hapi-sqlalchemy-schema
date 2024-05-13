from datetime import datetime

data_population = [
    # total national
    dict(
        id=1,
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        gender_code=None,
        age_range_code=None,
        population=1_000_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
        source_data="DATA,DATA,DATA",
    ),
    # national f, all ages
    dict(
        id=2,
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        gender_code="f",
        age_range_code=None,
        population=500_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
        source_data="DATA,DATA,DATA",
    ),
    # admin1 f, age 0-4
    dict(
        id=3,
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=2,
        gender_code="f",
        age_range_code="0-4",
        population=5_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
        source_data="DATA,DATA,DATA",
    ),
    # admin2 ages 80+
    dict(
        id=4,
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=4,
        gender_code=None,
        age_range_code="80+",
        population=500,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
        source_data="DATA,DATA,DATA",
    ),
]
