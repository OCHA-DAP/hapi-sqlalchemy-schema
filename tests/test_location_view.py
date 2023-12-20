from hdx.database.views import build_view

from hapi_schema.db_location import view_params_location


def test_location_view(run_view_test):
    """Check that location view has some columns."""
    view_location = build_view(view_params_location.__dict__)
    run_view_test(
        view=view_location,
        whereclause=(
            view_location.c.id == 1,
            view_location.c.code == "FOO",
            view_location.c.name == "Foolandia",
        ),
    )
