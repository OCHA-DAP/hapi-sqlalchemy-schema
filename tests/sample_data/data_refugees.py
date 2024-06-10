from datetime import datetime

data_refugees = [
    dict(
        resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
        origin_location_ref="1",
        asylum_location_ref="2",
        population_group="REF",
        gender="f",
        age_range="children",
        min_age="5",
        max_age="12",
        population="5000",
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 12, 31),
    ),
    dict(
        resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
        origin_location_ref="1",
        asylum_location_ref="2",
        population_group="ASY",
        gender="f",
        age_range="children",
        min_age="5",
        max_age="12",
        population="3000",
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 12, 31),
    ),
]
