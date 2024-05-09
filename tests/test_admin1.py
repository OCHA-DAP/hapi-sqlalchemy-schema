from datetime import datetime

from hdx.database import Database

from hapi_schema.db_admin1 import DBAdmin1, view_params_admin1


def test_admin1_view(run_view_test):
    """Check that admin1 view references location."""
    view_admin1 = Database.prepare_view(view_params_admin1.__dict__)
    run_view_test(
        view=view_admin1,
        whereclause=(
            view_admin1.c.id == 1,
            view_admin1.c.location_code == "FOO",
        ),
    )


def test_admin1_vat(run_indexes_test, run_columns_test):
    """Check that the admin1 view as table is correct - columns match, expected indexes present"""
    expected_indexes = [
        "location_code",
        "location_name",
        "reference_period_start",
        "reference_period_end",
    ]
    run_columns_test("admin1_vat", "admin1_view", view_params_admin1)
    run_indexes_test("admin1_vat", expected_indexes)


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBAdmin1(
                location_ref=1,
                code="FOO-003",
                name="Province 3",
                is_unspecified=False,
                reference_period_start=datetime(2023, 1, 2),
                reference_period_end=datetime(2023, 1, 1),
            )
        ],
        expected_constraint="reference_period",
    )


def test_code_date_unique(run_constraints_test):
    """Check that reference_period_start and code must be unique together"""
    run_constraints_test(
        new_rows=[
            DBAdmin1(
                location_ref=1,
                code="FOO-003",
                name="Province 3",
                is_unspecified=False,
                reference_period_start=datetime(2023, 1, 1),
            ),
            DBAdmin1(
                location_ref=1,
                code="FOO-003",
                name="Province 3",
                is_unspecified=False,
                reference_period_start=datetime(2023, 1, 1),
            ),
        ],
        expected_constraint="admin1_code_and_reference_period_unique",
    )
