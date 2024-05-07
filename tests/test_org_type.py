from hdx.database import Database

from hapi_schema.db_org_type import view_params_org_type


def test_org_type_view(run_view_test):
    """Check that org type has all fields."""
    (dict(code="433", description="Donor"),)
    view_org_type = Database.prepare_view(view_params_org_type.__dict__)
    run_view_test(
        view=view_org_type,
        whereclause=(
            view_org_type.c.code == "433",
            view_org_type.c.description == "Donor",
        ),
    )
