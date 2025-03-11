from datetime import datetime

import pytest
from hdx.database import Database

from hapi_schema.db_rainfall import DBRainfall, view_params_rainfall
from hapi_schema.utils.enums import TimePeriod, Version
from hapi_schema.views import prepare_hapi_views


def test_rainfall_view(run_view_test):
    """Check that rainfall references other tables."""
    view_rainfall = Database.prepare_view(view_params_rainfall.__dict__)
    run_view_test(
        view=view_rainfall,
        whereclause=(
            view_rainfall.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_rainfall.c.provider_admin1_code == "393",
            view_rainfall.c.provider_admin2_code == "39339",
            view_rainfall.c.admin2_code == "FOO-001-XXX",
            view_rainfall.c.admin1_code == "FOO-001",
            view_rainfall.c.location_code == "FOO",
            view_rainfall.c.admin_level == 2,
        ),
    )


def test_rainfall_availability(run_view_test):
    view_availability = prepare_hapi_views()["data_availability"]
    run_view_test(
        view=view_availability,
        whereclause=(
            view_availability.c.category == "climate",
            view_availability.c.subcategory == "hazards-rainfall",
            view_availability.c.location_code == "FOO",
            view_availability.c.admin1_name == "Province 01",
            view_availability.c.admin2_name == "District A",
            view_availability.c.hapi_updated_date == datetime(2023, 6, 1),
        ),
    )


@pytest.fixture
def base_parameters():
    return dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        provider_admin1_code="393",
        provider_admin2_code="39339",
        time_period=TimePeriod.DEAKD,
        rainfall=4.8571,
        rainfall_long_term_average=9.4095,
        rainfall_anomaly_pct=68.4071,
        number_pixels=7,
        version=Version.FINAL,
        reference_period_start=datetime(2020, 1, 1),
        reference_period_end=datetime(2020, 1, 10),
    )


def test_reference_period_constraint(run_constraints_test, base_parameters):
    """Check that reference_period_end cannot be less than start"""
    modified_params = {
        **base_parameters,
        **dict(
            reference_period_start=datetime(2023, 1, 2),
            reference_period_end=datetime(2023, 1, 1),
        ),
    }
    run_constraints_test(
        new_rows=[DBRainfall(**modified_params)],
        expected_constraint="reference_period_constraint",
    )


def test_rainfall_positive(run_constraints_test, base_parameters):
    """Check that the rainfall value is positive"""
    modified_params = {**base_parameters, "rainfall": -1.0345}
    run_constraints_test(
        new_rows=[
            DBRainfall(**modified_params),
        ],
        expected_constraint="rainfall_constraint",
    )


def test_rainfall_long_term_average_positive(run_constraints_test, base_parameters):
    """Check that the rainfall value is positive"""
    modified_params = {**base_parameters, "rainfall_long_term_average": -1.0345}
    run_constraints_test(
        new_rows=[
            DBRainfall(**modified_params),
        ],
        expected_constraint="rainfall_long_term_average_constraint",
    )


def test_rainfall_anomaly_pct_positive(run_constraints_test, base_parameters):
    """Check that the rainfall value is positive"""
    modified_params = {**base_parameters, "rainfall_anomaly_pct": -1.0345}
    run_constraints_test(
        new_rows=[
            DBRainfall(**modified_params),
        ],
        expected_constraint="rainfall_anomaly_pct_constraint",
    )


def test_number_pixels_positive(run_constraints_test, base_parameters):
    """Check that the rainfall value is positive"""
    modified_params = {**base_parameters, "number_pixels": 0}
    run_constraints_test(
        new_rows=[
            DBRainfall(**modified_params),
        ],
        expected_constraint="number_pixels_constraint",
    )
