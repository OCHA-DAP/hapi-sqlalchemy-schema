from hdx.database.views import build_view

from hapi_schema.db_org import view_params_org


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
