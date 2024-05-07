from datetime import datetime

from hdx.database import Database

from hapi_schema.db_population import DBPopulation, view_params_population
from hapi_schema.utils.enums import Gender


def test_population_view(run_view_test):
    """Check that population references other tables."""
    view_population = Database.prepare_view(view_params_population.__dict__)
    run_view_test(
        view=view_population,
        whereclause=(
            view_population.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_population.c.admin2_code == "FOO-001-XXX",
            view_population.c.admin1_code == "FOO-001",
            view_population.c.location_code == "FOO",
            view_population.c.gender == "f",
        ),
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBPopulation(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=1,
                gender=Gender.ALL,
                population=1_000_000,
                reference_period_start=datetime(2023, 1, 2),
                reference_period_end=datetime(2023, 1, 1),
            )
        ],
        expected_constraint="reference_period",
    )


def test_population_positive(run_constraints_test):
    """Check that the population value is positive"""
    run_constraints_test(
        new_rows=[
            DBPopulation(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=1,
                gender=Gender.ALL,
                population=-1,
                reference_period_start=datetime(2023, 1, 1),
                reference_period_end=datetime(2023, 1, 2),
            ),
        ],
        expected_constraint="population",
    )


def test_minage_positive(run_constraints_test):
    """Check that the min_age value is positive"""
    run_constraints_test(
        new_rows=[
            DBPopulation(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=1,
                gender=Gender.ALL,
                age_range="-1-20",
                min_age=-1,
                max_age=20,
                population=1_000_000,
                reference_period_start=datetime(2023, 1, 1),
                reference_period_end=datetime(2023, 1, 2),
            ),
        ],
        expected_constraint="min_age",
    )


def test_maxage_positive(run_constraints_test):
    """Check that the max_age value is positive"""
    run_constraints_test(
        new_rows=[
            DBPopulation(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=1,
                gender=Gender.ALL,
                age_range="0--1",
                min_age=0,
                max_age=-1,
                population=1_000_000,
                reference_period_start=datetime(2023, 1, 1),
                reference_period_end=datetime(2023, 1, 2),
            ),
        ],
        expected_constraint="max_age",
    )
