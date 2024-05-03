from datetime import datetime

from hdx.database.views import build_view

from hapi_schema.db_population import DBPopulation, view_params_population


def test_population_view(run_view_test):
    """Check that population references other tables."""
    view_population = build_view(view_params_population.__dict__)
    run_view_test(
        view=view_population,
        whereclause=(
            view_population.c.dataset_hdx_id
            == "c3f001fa-b45b-464c-9460-1ca79fd39b40",
            view_population.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_population.c.resource_name == "resource-01.csv",
            view_population.c.admin2_code == "FOO-001-XXX",
            view_population.c.admin1_code == "FOO-001",
            view_population.c.location_code == "FOO",
            view_population.c.gender_marker == "f",
        ),
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBPopulation(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=1,
                gender_marker="*",
                age_range="*",
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
                gender_marker="*",
                age_range="*",
                population=-1,
                reference_period_start=None,
                reference_period_end=None,
                source_data="DATA,DATA,DATA",
            ),
        ],
        expected_constraint="population",
    )
