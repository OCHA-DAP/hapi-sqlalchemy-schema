from datetime import datetime

data_humanitarian_needs = [
    # total national
    dict(
        id=1,
        resource_ref=1,
        admin2_ref=1,
        gender_code=None,
        age_range_code=None,
        is_disabled=None,
        sector_code=None,
        in_need=1_000_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
        source_data="DATA,DATA,DATA",
    ),
    # national f, all ages, disabled, sector SHL
    dict(
        id=2,
        resource_ref=1,
        admin2_ref=1,
        gender_code="f",
        age_range_code=None,
        is_disabled=True,
        sector_code="SHL",
        in_need=500_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
        source_data="DATA,DATA,DATA",
    ),
    # admin1 f, age 0-4, not disabled, sector WSH
    dict(
        id=3,
        resource_ref=1,
        admin2_ref=2,
        gender_code="f",
        age_range_code="0-4",
        is_disabled=False,
        sector_code="WSH",
        in_need=5_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
        source_data="DATA,DATA,DATA",
    ),
    # admin2 ages 80+, disabled, sector HEA
    dict(
        id=4,
        resource_ref=1,
        admin2_ref=4,
        gender_code=None,
        age_range_code="80+",
        is_disabled=True,
        sector_code="HEA",
        in_need=500,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 6, 30),
        source_data="DATA,DATA,DATA",
    ),
]
