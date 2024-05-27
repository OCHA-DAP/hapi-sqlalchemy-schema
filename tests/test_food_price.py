from datetime import datetime

from hdx.database import Database

from hapi_schema.db_food_price import (
    DBFoodPrice,
    view_params_food_price,
)


def test_food_price_view(run_view_test):
    """Check that national risk references other tables."""
    view_food_price = Database.prepare_view(view_params_food_price.__dict__)
    run_view_test(
        view=view_food_price,
        whereclause=(
            view_food_price.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_food_price.c.commodity_code == "001",
            view_food_price.c.currency_code == "FOO",
            view_food_price.c.price_flag == "actual",
            view_food_price.c.price_type == "Retail",
            view_food_price.c.unit == "basket",
            view_food_price.c.price == 100.00,
            view_food_price.c.admin2_ref == 4,
            view_food_price.c.market_name == "Market #1",
            view_food_price.c.lat == 0.1,
            view_food_price.c.lon == -0.1,
            view_food_price.c.commodity_category == "vegetables and fruits",
            view_food_price.c.commodity_name == "Commodity #1",
            view_food_price.c.location_name == "Foolandia",
            view_food_price.c.admin1_name == "Province 01",
            view_food_price.c.admin2_name == "District A",
        ),
    )


def test_price_not_negative_constraint(run_constraints_test):
    """Check constraint that price is not negative"""
    data = _sample_data()
    data["price"] = -1.0
    run_constraints_test(
        new_rows=[
            DBFoodPrice(**data),
        ],
        expected_constraint="price_constraint",
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    data = _sample_data()
    data["reference_period_start"] = datetime(2025, 1, 1)
    run_constraints_test(
        new_rows=[
            DBFoodPrice(**data),
        ],
        expected_constraint="reference_period_constraint",
    )


# Utility functions


def _sample_data():
    # return a valid record (tests may change individual fields)
    return dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        market_code="001",
        commodity_code="001",
        currency_code="FOO",
        unit="basket",
        price_flag="actual",
        price_type="Retail",
        price=100.00,
        reference_period_start=datetime(2024, 1, 1),
        reference_period_end=datetime(2024, 1, 31),
    )
