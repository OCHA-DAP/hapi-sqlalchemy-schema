from datetime import datetime

data_conflict_event = [
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=4,
        provider_admin1_name="Provincia 01",
        provider_admin2_name="Distrito A",
        event_type="political_violence",
        events=10,
        fatalities=2,
        reference_period_start=datetime(2024, 1, 1),
        reference_period_end=datetime(2024, 1, 31),
    ),
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        provider_admin1_name="Provincia 01",
        provider_admin2_name="Distrito A",
        event_type="civilian_targeting",
        events=3,
        fatalities=0,
        reference_period_start=datetime(2024, 1, 1),
        reference_period_end=datetime(2024, 1, 31),
    ),
]
