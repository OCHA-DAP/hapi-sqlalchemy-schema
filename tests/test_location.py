from datetime import datetime

from hdx.database.views import build_view

from hapi_schema.db_location import DBLocation, view_params_location


def test_location_view(run_view_test):
    """Check that location view has some columns."""
    view_location = build_view(view_params_location.__dict__)
    run_view_test(
        view=view_location,
        whereclause=(
            view_location.c.id == 1,
            view_location.c.code == "FOO",
            view_location.c.name == "Foolandia",
        ),
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBLocation(
                code="BAR",
                name="Barlandia",
                reference_period_start=datetime(2023, 1, 2),
                reference_period_end=datetime(2023, 1, 1),
                hapi_updated_date=datetime(2023, 1, 1),
                hapi_replaced_date=None,
            )
        ],
        expected_constraint="reference_period",
    )


def test_hapi_date_constraint(run_constraints_test):
    """Check that hapi_replaced_date cannot be less than hapi_udpated_date"""
    run_constraints_test(
        new_rows=[
            DBLocation(
                code="BAR",
                name="Barlandia",
                reference_period_start=None,
                reference_period_end=None,
                hapi_updated_date=datetime(2023, 1, 2),
                hapi_replaced_date=datetime(2023, 1, 1),
            )
        ],
        expected_constraint="hapi_dates",
    )


def test_code_date_unique(run_constraints_test):
    """Check that hapi_updated_date and code must be unique together"""
    run_constraints_test(
        new_rows=[
            DBLocation(
                code="BAR",
                name="Barlandia",
                reference_period_start=None,
                reference_period_end=None,
                hapi_updated_date=datetime(2023, 1, 1),
                hapi_replaced_date=None,
            ),
            DBLocation(
                code="BAR",
                name="Barlandia",
                reference_period_start=None,
                reference_period_end=None,
                hapi_updated_date=datetime(2023, 1, 1),
                hapi_replaced_date=None,
            ),
        ],
        expected_constraint="UNIQUE constraint failed",
    )
