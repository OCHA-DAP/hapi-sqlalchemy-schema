from hdx.database import Database

from hapi_schema.db_wfp_market import (
    DBWFPMarket,
    view_params_wfp_market,
)


def test_wfp_market_view(run_view_test):
    """Check that wfp_market view shows some columns."""
    view_wfp_market = Database.prepare_view(view_params_wfp_market.__dict__)
    run_view_test(
        view=view_wfp_market,
        whereclause=(
            view_wfp_market.c.code == "001",
            view_wfp_market.c.name == "Market #1",
            view_wfp_market.c.lat == 0.1,
            view_wfp_market.c.lon == -0.1,
            view_wfp_market.c.location_name == "Foolandia",
            view_wfp_market.c.admin1_name == "Province 01",
            view_wfp_market.c.admin2_name == "District A",
        ),
    )


def test_lat_constraint(run_constraints_test):
    """Check that latlon constraint works with latitude"""
    data = _sample_data()
    data["lat"] = 91
    run_constraints_test(
        new_rows=[
            DBWFPMarket(**data),
        ],
        expected_constraint="latlon_constraint",
    )


def test_lon_constraint(run_constraints_test):
    """Check that latlon constraint works with longitude"""
    data = _sample_data()
    data["lon"] = -181
    run_constraints_test(
        new_rows=[
            DBWFPMarket(**data),
        ],
        expected_constraint="latlon",
    )


# Util functions


def _sample_data():
    # return the whole record, then tests can change as needed
    return dict(
        code="001",
        admin2_ref=4,
        name="Market #1",
        lat=0.1,
        lon=-0.1,
    )
