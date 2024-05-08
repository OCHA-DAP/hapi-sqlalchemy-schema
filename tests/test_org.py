from hdx.database import Database

from hapi_schema.db_org import view_params_org


def test_org_view(run_view_test):
    """Check that org view references org type."""
    view_org = Database.prepare_view(view_params_org.__dict__)
    run_view_test(
        view=view_org,
        whereclause=(
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
