from hdx.database import Database

from hapi_schema.db_wfp_commodity import view_params_wfp_commodity


def test_wfp_commodity_view(run_view_test):
    """Check that wfp_commodity view shows some columns."""
    view_wfp_commodity = Database.prepare_view(
        view_params_wfp_commodity.__dict__
    )
    run_view_test(
        view=view_wfp_commodity,
        whereclause=(
            view_wfp_commodity.c.code == "SHL",
            view_wfp_commodity.c.name == "Emergency Shelter and NFI",
        ),
    )
