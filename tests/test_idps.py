from datetime import datetime

import pytest
from hdx.database import Database

from hapi_schema.db_idps import (
    DBIDPs,
    view_params_idps,
)
from hapi_schema.views import prepare_hapi_views


def test_idps_view(run_view_test):
    """Check idps view has all columns."""
    view_idps = Database.prepare_view(view_params_idps.__dict__)
    run_view_test(
        view=view_idps,
        whereclause=(
            view_idps.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_idps.c.admin2_ref == 2,
            view_idps.c.provider_admin1_name == "Provincia 01",
            view_idps.c.provider_admin2_name == "Distrito B",
            view_idps.c.assessment_type == "BA",
            view_idps.c.reporting_round == 18,
            view_idps.c.operation == "Operation",
            view_idps.c.population == 25000,
            view_idps.c.admin2_code == "FOO-001-XXX",
            view_idps.c.admin1_code == "FOO-001",
            view_idps.c.location_code == "FOO",
            view_idps.c.admin_level == 2,
        ),
    )


def test_idps_availability(run_view_test):
    view_availability = prepare_hapi_views()["data_availability"]
    run_view_test(
        view=view_availability,
        whereclause=(
            view_availability.c.category == "affected-people",
            view_availability.c.subcategory == "idps",
            view_availability.c.location_code == "FOO",
            view_availability.c.admin1_code == "FOO-001",
            view_availability.c.admin2_code == "FOO-001-XXX",
            view_availability.c.admin_level == 2,
            view_availability.c.hapi_updated_date == datetime(2023, 6, 1),
        ),
    )


@pytest.fixture
def base_parameters():
    return dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=2,
        provider_admin1_name="Provincia 01",
        provider_admin2_name="Distrito B",
        assessment_type="BA",
        reporting_round=18,
        operation="operation",
        population=25000,
        reference_period_start=datetime(2020, 1, 1),
        reference_period_end=datetime(2020, 1, 2),
    )


def test_reporting_round_constraint(run_constraints_test, base_parameters):
    """Check that the reporting round is greater than 0"""
    modified_params = {**base_parameters, "reporting_round": -1}
    run_constraints_test(
        new_rows=[
            DBIDPs(**modified_params),
        ],
        expected_constraint="reporting_round_constraint",
    )


def test_population_positive(run_constraints_test, base_parameters):
    """Check that the population value is positive"""
    modified_params = {**base_parameters, "population": -1}
    run_constraints_test(
        new_rows=[
            DBIDPs(**modified_params),
        ],
        expected_constraint="population_constraint",
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
        new_rows=[DBIDPs(**modified_params)],
        expected_constraint="reference_period_constraint",
    )
