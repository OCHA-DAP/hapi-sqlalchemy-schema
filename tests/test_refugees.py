from datetime import datetime

from hdx.database import Database

from hapi_schema.db_refugees import (
    DBRefugees,
    view_params_refugees,
)


def test_refugees_view(run_view_test):
    """Check that refugees view references other tables."""
    view_refugees = Database.prepare_view(view_params_refugees.__dict__)
    run_view_test(
        view=view_refugees,
        whereclause=(
            view_refugees.c.resource_hdx_id
            == "62ad6e55-5f5d-4494-854c-4110687e9e25",
            view_refugees.c.origin_location_code == "FOO",
            view_refugees.c.asylum_location_code == "BAR",
        ),
    )


def test_min_age(run_constraints_test):
    """Check that the minimum age is greater than 0"""
    run_constraints_test(
        new_rows=[
            DBRefugees(
                resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
                origin_location_ref=1,
                asylum_location_ref=2,
                population_group="REF",
                gender="f",
                age_range="children",
                min_age=-5,
                max_age=12,
                population=2000,
                reference_period_start=datetime(2023, 1, 1),
                reference_period_end=datetime(2023, 12, 31),
            )
        ],
        expected_constraint="min_age_constraint",
    )


def test_max_age(run_constraints_test):
    """Check that the max age is greater than 0"""
    run_constraints_test(
        new_rows=[
            DBRefugees(
                resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
                origin_location_ref=1,
                asylum_location_ref=2,
                population_group="REF",
                gender="f",
                age_range="children",
                min_age=5,
                max_age=-1,
                population=2000,
                reference_period_start=datetime(2023, 1, 1),
                reference_period_end=datetime(2023, 12, 31),
            )
        ],
        expected_constraint="max_age_constraint",
    )


def test_population_positive(run_constraints_test):
    """Check that the population value is positive"""
    run_constraints_test(
        new_rows=[
            DBRefugees(
                resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
                origin_location_ref=1,
                asylum_location_ref=2,
                population_group="REF",
                gender="f",
                age_range="children",
                min_age=5,
                max_age=12,
                population=-2000,
                reference_period_start=datetime(2023, 1, 1),
                reference_period_end=datetime(2023, 12, 31),
            )
        ],
        expected_constraint="population_constraint",
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBRefugees(
                resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
                origin_location_ref=1,
                asylum_location_ref=2,
                population_group="REF",
                gender="f",
                age_range="children",
                min_age=5,
                max_age=12,
                population=2000,
                reference_period_start=datetime(2023, 2, 1),
                reference_period_end=datetime(2023, 1, 1),
            )
        ],
        expected_constraint="reference_period_constraint",
    )
