from datetime import datetime

from hdx.database import Database

from hapi_schema.db_admin2 import DBAdmin2, view_params_admin2


def test_admin2_view(run_view_test):
    """Check that admin2 view references admin1 and location."""
    view_admin2 = Database.prepare_view(view_params_admin2.__dict__)
    run_view_test(
        view=view_admin2,
        whereclause=(
            view_admin2.c.id == 1,
            view_admin2.c.admin1_code == "FOO-XXX",
            view_admin2.c.location_code == "FOO",
        ),
    )


def test_admin2_vat(run_indexes_test, run_columns_test, run_primary_keys_test):
    """Check that the view as table is correct - columns match, expected indexes present"""
    expected_primary_keys = ["id"]
    expected_indexes = [
        "code",
        "name",
        "reference_period_start",
        "reference_period_end",
        "location_code",
        "location_name",
        "admin1_code",
        "admin1_name",
    ]
    run_columns_test("admin2_vat", "admin2_view", view_params_admin2)
    run_indexes_test("admin2_vat", expected_indexes)
    run_primary_keys_test("admin2_vat", expected_primary_keys)


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBAdmin2(
                admin1_ref=3,
                code="FOO-002-D",
                name="District D",
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
            DBAdmin2(
                admin1_ref=3,
                code="FOO-002-D",
                name="District D",
                is_unspecified=False,
                reference_period_start=datetime(2023, 1, 1),
            ),
            DBAdmin2(
                admin1_ref=3,
                code="FOO-002-D",
                name="District D",
                is_unspecified=False,
                reference_period_start=datetime(2023, 1, 1),
            ),
        ],
        expected_constraint="admin2_code_and_reference_period_unique",
    )
