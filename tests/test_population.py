from datetime import datetime

import pytest
from hdx.database import Database

from hapi_schema.db_population import DBPopulation, view_params_population
from hapi_schema.utils.enums import Gender
from hapi_schema.views import prepare_hapi_views


def test_population_view(run_view_test):
    """Check that population references other tables."""
    view_population = Database.prepare_view(view_params_population.__dict__)
    run_view_test(
        view=view_population,
        whereclause=(
            view_population.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_population.c.provider_admin1_name == "Provincia 01",
            view_population.c.provider_admin2_name == "Distrito A",
            view_population.c.admin2_code == "FOO-001-XXX",
            view_population.c.admin1_code == "FOO-001",
            view_population.c.location_code == "FOO",
            view_population.c.gender == "f",
            view_population.c.admin_level == 2,
        ),
    )


def test_population_availability(run_view_test):
    view_availability = prepare_hapi_views()["data_availability"]
    run_view_test(
        view=view_availability,
        whereclause=(
            view_availability.c.category == "population-social",
            view_availability.c.subcategory == "population",
            view_availability.c.location_code == "FOO",
            view_availability.c.admin1_name == "Province 01",
            view_availability.c.admin2_name == "District A",
            view_availability.c.admin_level == 2,
            view_availability.c.hapi_updated_date == datetime(2023, 6, 1),
        ),
    )


@pytest.fixture
def base_parameters():
    return dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        provider_admin1_name="Provincia 01",
        provider_admin2_name="Distrito A",
        gender=Gender.ALL,
        age_range="all",
        population=1_000_000,
        reference_period_start=datetime(2020, 1, 1),
        reference_period_end=datetime(2020, 1, 2),
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
        new_rows=[DBPopulation(**modified_params)],
        expected_constraint="reference_period_constraint",
    )


def test_population_positive(run_constraints_test, base_parameters):
    """Check that the population value is positive"""
    modified_params = {**base_parameters, "population": -1}
    run_constraints_test(
        new_rows=[
            DBPopulation(**modified_params),
        ],
        expected_constraint="population_constraint",
    )


def test_minage(run_constraints_test, base_parameters):
    """Check that the min_age value is positive, and NULL if
    age_range is all"""
    modified_params = {**base_parameters, **dict(age_range="5-10", min_age=-1)}
    run_constraints_test(
        new_rows=[
            DBPopulation(**modified_params),
        ],
        expected_constraint="min_age_constraint",
    )
    modified_params = {
        **base_parameters,
        **dict(age_range="all", min_age="10"),
    }
    print(modified_params)
    run_constraints_test(
        new_rows=[
            DBPopulation(**modified_params),
        ],
        expected_constraint="min_age_constraint",
    )


def test_maxage(run_constraints_test, base_parameters):
    """Check that the max_age is > min_age, and NULL when min_age is NULL"""
    modified_params = {
        **base_parameters,
        **dict(age_range="5-10", min_age=5, max_age=4),
    }
    run_constraints_test(
        new_rows=[
            DBPopulation(**modified_params),
        ],
        expected_constraint="max_age_constraint",
    )
    modified_params = {
        **base_parameters,
        **dict(age_range="unknown", min_age=None, max_age=10),
    }
    run_constraints_test(
        new_rows=[
            DBPopulation(**modified_params),
        ],
        expected_constraint="max_age_constraint",
    )
