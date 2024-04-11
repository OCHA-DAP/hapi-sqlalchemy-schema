from hdx.database.views import build_view

from hapi_schema.db_population_status import view_params_population_status


def test_population_status_view(run_view_test):
    """Check gender view has all columns."""
    view_population_status = build_view(view_params_population_status.__dict__)
    run_view_test(
        view=view_population_status,
        whereclause=(
            view_population_status.c.code == "inneed",
            view_population_status.c.description == "number of people in need",
        ),
    )
