from hdx.database.views import build_view

from hapi_schema.db_admin2 import view_params_admin2


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
