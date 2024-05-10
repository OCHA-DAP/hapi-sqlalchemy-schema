from datetime import datetime

from hdx.database import Database

from hapi_schema.db_funding import (
    DBFunding,
    view_params_funding,
)


def test_funding_view(run_view_test):
    """Check gender view has all columns."""
    view_funding = Database.prepare_view(view_params_funding.__dict__)
    run_view_test(
        view=view_funding,
        whereclause=(
            view_funding.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_funding.c.appeal_code == "HFOO24",
            view_funding.c.location_ref == 1,
            view_funding.c.appeal_name == "Foolandia HRP 2024",
            view_funding.c.appeal_type == "HRP",
            view_funding.c.requirements_usd == 100000.0,
            view_funding.c.funding_usd == 50000.0,
            view_funding.c.funding_pct == 50.0,
            view_funding.c.location_code == "FOO",
            view_funding.c.location_name == "Foolandia",
        ),
    )


def test_food_security_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that the food_security view as table is correct - columns match, expected indexes present"""
    expected_primary_keys = ["appeal_code", "location_ref"]
    expected_indexes = [
        "requirements_usd",
        "funding_usd",
        "funding_pct",
        "reference_period_start",
        "location_code",
        "location_name",
    ]
    run_columns_test("funding_vat", "funding_view", view_params_funding)
    run_indexes_test("funding_vat", expected_indexes)
    run_primary_keys_test("funding_vat", expected_primary_keys)


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBFunding(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                appeal_code="HFOO24",
                location_ref=1,
                appeal_name="Foolandia HRP 2024",
                appeal_type="HRP",
                requirements_usd=100000.0,
                funding_usd=50000.0,
                funding_pct=50,
                reference_period_start=datetime(2025, 1, 1),
                reference_period_end=datetime(2024, 12, 31),
            ),
        ],
        expected_constraint="reference_period",
    )


def test_requirements_usd_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBFunding(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                appeal_code="HFOO24",
                location_ref=1,
                appeal_name="Foolandia HRP 2024",
                appeal_type="HRP",
                requirements_usd=-100000.0,
                funding_usd=50000.0,
                funding_pct=50,
                reference_period_start=datetime(2024, 1, 1),
                reference_period_end=datetime(2024, 12, 31),
            ),
        ],
        expected_constraint="requirements_usd",
    )


def test_funding_usd_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBFunding(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                appeal_code="HFOO24",
                location_ref=1,
                appeal_name="Foolandia HRP 2024",
                appeal_type="HRP",
                requirements_usd=100000.0,
                funding_usd=-50000.0,
                funding_pct=50,
                reference_period_start=datetime(2024, 1, 1),
                reference_period_end=datetime(2024, 12, 31),
            ),
        ],
        expected_constraint="funding_usd",
    )


def test_funding_pct_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBFunding(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                appeal_code="HFOO24",
                location_ref=1,
                appeal_name="Foolandia HRP 2024",
                appeal_type="HRP",
                requirements_usd=100000.0,
                funding_usd=50000.0,
                funding_pct=-50,
                reference_period_start=datetime(2024, 1, 1),
                reference_period_end=datetime(2024, 12, 31),
            ),
        ],
        expected_constraint="funding_pct",
    )
