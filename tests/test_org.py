from datetime import datetime

from hdx.database.views import build_view

from hapi_schema.db_org import DBOrg, view_params_org


def test_org_view(run_view_test):
    """Check that org view references org type."""
    view_org = build_view(view_params_org.__dict__)
    run_view_test(
        view=view_org,
        whereclause=(
            view_org.c.id == 1,
            view_org.c.org_type_code == "433",
            view_org.c.org_type_description == "Donor",
        ),
    )


def test_org_vat(run_indexes_test, run_columns_test):
    """Check that the org view as table is correct - columns match, expected indexes present"""
    expected_indexes = [
        "acronym",
        "org_type_description",
        "hapi_updated_date",
        "hapi_replaced_date",
        "reference_period_start",
        "reference_period_end",
    ]
    run_columns_test(
        "org_vat",
        "org_view",
        view_params_org,
    )
    run_indexes_test("org_vat", expected_indexes)


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBOrg(
                acronym="ORG04",
                name="Organisation 4",
                org_type_code="433",
                reference_period_start=datetime(2023, 1, 2),
                reference_period_end=datetime(2023, 1, 1),
                hapi_updated_date=datetime(2023, 1, 1),
                hapi_replaced_date=None,
            ),
        ],
        expected_constraint="reference_period",
    )


def test_hapi_date_constraint(run_constraints_test):
    """Check that hapi_replaced_date cannot be less than hapi_udpated_date"""
    run_constraints_test(
        new_rows=[
            DBOrg(
                acronym="ORG04",
                name="Organisation 4",
                org_type_code="433",
                reference_period_start=None,
                reference_period_end=None,
                hapi_updated_date=datetime(2023, 1, 2),
                hapi_replaced_date=datetime(2023, 1, 1),
            ),
        ],
        expected_constraint="hapi_dates",
    )
