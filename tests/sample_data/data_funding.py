from datetime import datetime

data_funding = [
    # appeal funding
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        appeal_code="HFOO24",
        location_ref=1,
        appeal_name="Foolandia HRP 2024",
        appeal_type="HRP",
        requirements_usd=100000.0,
        funding_usd=50000.0,
        funding_pct=50,
        reference_period_start=datetime(2024, 1, 1),
        reference_period_end=datetime(2024, 12, 31),
    ),
    # non-appeal funding
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        appeal_code="",
        location_ref=1,
        appeal_name="Not specified",
        appeal_type=None,
        requirements_usd=None,
        funding_usd=300000.0,
        funding_pct=None,
        reference_period_start=datetime(2024, 1, 1),
        reference_period_end=datetime(2024, 12, 31),
    ),
]
