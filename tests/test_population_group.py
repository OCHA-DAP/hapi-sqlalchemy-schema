from hdx.database.views import build_view

from hapi_schema.db_population_group import view_params_population_group


def test_population_group_view(run_view_test):
    """Check gender view has all columns."""
    view_population_group = build_view(view_params_population_group.__dict__)
    run_view_test(
        view=view_population_group,
        whereclause=(
            view_population_group.c.code == "idps",
            view_population_group.c.description
            == "internally displaced persons",
        ),
    )
