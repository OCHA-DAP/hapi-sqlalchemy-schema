from datetime import datetime

data_food_price = [
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=4,
        market_code="001",
        commodity_code="001",
        currency_code="FOO",
        unit="basket",
        price_flag="actual",
        price_type="Retail",
        price=100.00,
        reference_period_start=datetime(2024, 1, 1),
        reference_period_end=datetime(2024, 1, 31),
    ),
    dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        market_code="001",
        commodity_code="001",
        currency_code="FOO",
        unit="kilo",
        price_flag="aggregate",
        price_type="Wholesale",
        price=200.00,
        reference_period_start=datetime(2024, 1, 1),
        reference_period_end=datetime(2024, 1, 31),
    ),
]
