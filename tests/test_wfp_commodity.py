from hdx.database import Database

from hapi_schema.db_wfp_commodity import view_params_wfp_commodity


def test_wfp_commodity_view(run_view_test):
    """Check that wfp_commodity_view shows some columns."""
    view_wfp_commodity = Database.prepare_view(
        view_params_wfp_commodity.__dict__
    )
    run_view_test(
        view=view_wfp_commodity,
        whereclause=(
            view_wfp_commodity.c.code == "001",
            view_wfp_commodity.c.category == "vegetables and fruits",
            view_wfp_commodity.c.name == "Commodity #1",
        ),
    )
