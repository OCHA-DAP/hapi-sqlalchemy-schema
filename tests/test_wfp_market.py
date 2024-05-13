from hdx.database import Database

from hapi_schema.db_wfp_market import view_params_wfp_market


def test_wfp_market_view(run_view_test):
    """Check that wfp_market view shows some columns."""
    view_wfp_market = Database.prepare_view(view_params_wfp_market.__dict__)
    run_view_test(
        view=view_wfp_market,
        whereclause=(
            view_wfp_market.c.code == "SHL",
            view_wfp_market.c.name == "Emergency Shelter and NFI",
        ),
    )
