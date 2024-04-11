from hdx.database.views import build_view

from hapi_schema.db_age_range import view_params_age_range


def test_age_range_view(run_view_test):
    """Check that age range shows code and numbers."""
    view_age_range = build_view(view_params_age_range.__dict__)
    run_view_test(
        view=view_age_range,
        whereclause=(
            view_age_range.c.code == "0-4",
            view_age_range.c.age_min == 0,
            view_age_range.c.age_max == 4,
        ),
    )
