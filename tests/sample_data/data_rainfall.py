from datetime import datetime

data_rainfall = [
    # admin 1
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=2,
        provider_admin1_name="Not provided",
        provider_admin2_name="Not provided",
        provider_admin1_code="393",
        provider_admin2_code="39339",
        aggregation_period="dekad",
        rainfall=4.8571,
        rainfall_long_term_average=9.4095,
        rainfall_anomaly_pct=68.4071,
        number_pixels=7,
        version="final",
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 1, 10),
    ),
    # admin 2
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=4,
        provider_admin1_name="Not provided",
        provider_admin2_name="Not provided",
        provider_admin1_code="393",
        provider_admin2_code="",
        aggregation_period="dekad",
        rainfall=5.8571,
        rainfall_long_term_average=10.4095,
        rainfall_anomaly_pct=69.4071,
        number_pixels=5,
        version="final",
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 1, 10),
    ),
]
