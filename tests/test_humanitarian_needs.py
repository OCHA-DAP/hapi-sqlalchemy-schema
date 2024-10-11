from datetime import datetime

import pytest
from hdx.database import Database

from hapi_schema.db_humanitarian_needs import (
    DBHumanitarianNeeds,
    view_params_humanitarian_needs,
)
from hapi_schema.utils.enums import PopulationStatus
from hapi_schema.views import prepare_hapi_views


def test_humanitarian_needs_view(run_view_test):
    """Check that humanitarian needs references other tables."""
    view_humanitarian_needs = Database.prepare_view(
        view_params_humanitarian_needs.__dict__
    )
    run_view_test(
        view=view_humanitarian_needs,
        whereclause=(
            view_humanitarian_needs.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_humanitarian_needs.c.provider_admin1_name == "Provincia 01",
            view_humanitarian_needs.c.provider_admin2_name == "Distrito B",
            view_humanitarian_needs.c.provider_admin1_name == "Provincia 01",
            view_humanitarian_needs.c.provider_admin2_name == "Distrito B",
            view_humanitarian_needs.c.admin2_code == "FOO-001-XXX",
            view_humanitarian_needs.c.admin1_code == "FOO-001",
            view_humanitarian_needs.c.location_code == "FOO",
            view_humanitarian_needs.c.population_status == "INN",
            view_humanitarian_needs.c.category
            == "Female - Disabled - Baby - IDP",
            view_humanitarian_needs.c.sector_name
            == "Water Sanitation Hygiene",
        ),
    )


def test_humanitarian_needs_availability(run_view_test):
    view_availability = prepare_hapi_views()
    run_view_test(
        view=view_availability,
        whereclause=(
            view_availability.c.category == "affected-people",
            view_availability.c.subcategory == "humanitarian-needs",
            view_availability.c.location_code == "FOO",
            view_availability.c.admin1_name == "Province 01",
            view_availability.c.admin2_name == "District A",
            view_availability.c.hapi_updated_date == datetime(2023, 6, 1),
        ),
    )


@pytest.fixture(scope="module")
def base_parameters():
    return dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        provider_admin1_name="Provincia 01",
        provider_admin2_name="Distrito B",
        category="",
        sector_code="*",
        population_status=PopulationStatus.AFFECTED,
        population=1_000_000,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 1, 2),
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
        new_rows=[DBHumanitarianNeeds(**modified_params)],
        expected_constraint="reference_period",
    )


def test_population_positive(run_constraints_test, base_parameters):
    """Check that the population value is positive"""
    modified_params = {**base_parameters, "population": -1}
    run_constraints_test(
        new_rows=[
            DBHumanitarianNeeds(**modified_params),
        ],
        expected_constraint="population_constraint",
    )
