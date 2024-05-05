from datetime import datetime

from hdx.database.views import build_view

from hapi_schema.db_admin2 import DBAdmin2, view_params_admin2


def test_admin2_view(run_view_test):
    """Check that admin2 view references admin1 and location."""
    view_admin2 = build_view(view_params_admin2.__dict__)
    run_view_test(
        view=view_admin2,
        whereclause=(
            view_admin2.c.id == 1,
            view_admin2.c.admin1_code == "FOO-XXX",
            view_admin2.c.location_code == "FOO",
        ),
    )


def test_admin2_vat(run_indexes_test, run_columns_test):
    """Check that the view as table is correct - columns match, expected indexes present"""
    expected_indexes = [
        "reference_period_start",
        "reference_period_end",
        "hapi_updated_date",
        "hapi_replaced_date",
    ]
    run_columns_test("admin2_vat", "admin2_view", view_params_admin2)
    run_indexes_test("admin2_vat", expected_indexes)


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
            DBAdmin2(
                admin1_ref=3,
                code="FOO-002-D",
                name="District D",
                is_unspecified=False,
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
            DBAdmin2(
                admin1_ref=3,
                code="FOO-002-D",
                name="District D",
                is_unspecified=False,
                reference_period_start=None,
                reference_period_end=None,
                hapi_updated_date=datetime(2023, 1, 1),
                hapi_replaced_date=None,
            ),
            DBAdmin2(
                admin1_ref=3,
                code="FOO-002-D",
                name="District D",
                is_unspecified=False,
                reference_period_start=None,
                reference_period_end=None,
                hapi_updated_date=datetime(2023, 1, 1),
                hapi_replaced_date=None,
            ),
        ],
        expected_constraint="UNIQUE constraint failed",
    )
