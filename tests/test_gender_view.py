from hdx.database.views import build_view

from hapi_schema.db_gender import view_params_gender


def test_gender_view(run_view_test):
    """Check gender view has all columns."""
    view_gender = build_view(view_params_gender.__dict__)
    run_view_test(
        view=view_gender,
        whereclause=(
            view_gender.c.code == "f",
            view_gender.c.description == "female",
        ),
    )
