from datetime import datetime

from hdx.database.views import build_view

from hapi_schema.db_org import DBOrg, view_params_org


def test_org_view(run_view_test):
    """Check that org view references org type."""
    view_org = build_view(view_params_org.__dict__)
    run_view_test(
        view=view_org,
        whereclause=(
            view_org.c.ident == "611c255706bfb8370827cba2a149a45f",
            view_org.c.org_type_code == "433",
            view_org.c.org_type_description == "Donor",
        ),
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBOrg(
                ident="c63b58971ace74c5f473d14a4325963b",
                acronym="ORG04",
                name="Organisation 4",
                org_type_code="433",
                reference_period_start=datetime(2023, 1, 2),
                reference_period_end=datetime(2023, 1, 1),
            ),
        ],
        expected_constraint="reference_period",
    )


def test_name_acronym_unique_constraint(run_constraints_test):
    """Check that name and acronym together must be unique"""
    run_constraints_test(
        new_rows=[
            DBOrg(
                ident="c63b58971ace74c5f473d14a4325963b",
                acronym="ORG04",
                name="Organisation 4",
                org_type_code="433",
                reference_period_start=datetime(2023, 1, 1),
                reference_period_end=datetime(2023, 1, 2),
            ),
            DBOrg(
                ident="7005be38b92e8589e823b6d86e72040e",
                acronym="ORG04",
                name="Organisation 4",
                org_type_code="437",
                reference_period_start=datetime(2024, 1, 1),
                reference_period_end=datetime(2024, 1, 2),
            ),
        ],
        expected_constraint="UNIQUE constraint failed",
    )
