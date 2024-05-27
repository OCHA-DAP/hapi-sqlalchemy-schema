from datetime import datetime

from hdx.database import Database

from hapi_schema.db_location import DBLocation, view_params_location


def test_location_view(run_view_test):
    """Check that location view has some columns."""
    view_location = Database.prepare_view(view_params_location.__dict__)
    run_view_test(
        view=view_location,
        whereclause=(
            view_location.c.id == 1,
            view_location.c.code == "FOO",
            view_location.c.name == "Foolandia",
        ),
    )


def test_location_defaults(run_view_test):
    """Check that default values are set properly."""
    view_location = Database.prepare_view(view_params_location.__dict__)
    run_view_test(
        view=view_location,
        whereclause=(
            view_location.c.id == 1,
            view_location.c.from_cods,  # should be True
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
            )
        ],
        expected_constraint="reference_period_constraint",
    )


def test_code_date_unique(run_constraints_test):
    """Check that reference_period_start and code must be unique together"""
    run_constraints_test(
        new_rows=[
            DBLocation(
                code="BAR",
                name="Barlandia",
                reference_period_start=datetime(2023, 1, 1),
            ),
            DBLocation(
                code="BAR",
                name="Barlandia",
                reference_period_start=datetime(2023, 1, 1),
            ),
        ],
        expected_constraint="location_code_and_reference_period_unique_constraint",
    )
