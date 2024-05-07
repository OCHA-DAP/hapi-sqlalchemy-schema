from datetime import datetime

from hdx.database import Database

from hapi_schema.db_humanitarian_needs import (
    DBHumanitarianNeeds,
    view_params_humanitarian_needs,
)
from hapi_schema.utils.enums import (
    DisabledMarker,
    Gender,
    PopulationGroup,
    PopulationStatus,
)


def test_humanitarian_needs_view(run_view_test):
    """Check that humanitarian needs references other tables."""
    view_humanitarian_needs = Database.prepare_view(
        view_params_humanitarian_needs.__dict__
    )
    run_view_test(
        view=view_humanitarian_needs,
        whereclause=(
            view_humanitarian_needs.c.dataset_hdx_id
            == "c3f001fa-b45b-464c-9460-1ca79fd39b40",
            view_humanitarian_needs.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_humanitarian_needs.c.resource_name == "resource-01.csv",
            view_humanitarian_needs.c.admin2_code == "FOO-001-XXX",
            view_humanitarian_needs.c.admin1_code == "FOO-001",
            view_humanitarian_needs.c.location_code == "FOO",
            view_humanitarian_needs.c.population_status == "INN",
            view_humanitarian_needs.c.population_group == "IDP",
            view_humanitarian_needs.c.sector_name
            == "Water Sanitation Hygiene",
            view_humanitarian_needs.c.gender == "f",
            view_humanitarian_needs.c.disabled_marker == "y",  # noqa: E712
        ),
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBHumanitarianNeeds(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=1,
                gender=Gender.ALL,
                disabled_marker=DisabledMarker.ALL,
                sector_code="*",
                population_group=PopulationGroup.ALL,
                population_status=PopulationStatus.AFFECTED,
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
            DBHumanitarianNeeds(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=1,
                gender=Gender.ALL,
                disabled_marker=DisabledMarker.ALL,
                sector_code="*",
                population_group=PopulationGroup.ALL,
                population_status=PopulationStatus.AFFECTED,
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
            DBHumanitarianNeeds(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=1,
                gender=Gender.ALL,
                age_range="-1-20",
                min_age=-1,
                max_age=20,
                disabled_marker=DisabledMarker.ALL,
                sector_code="*",
                population_group=PopulationGroup.ALL,
                population_status=PopulationStatus.AFFECTED,
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
            DBHumanitarianNeeds(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=1,
                gender=Gender.ALL,
                age_range="0--1",
                min_age=0,
                max_age=-1,
                disabled_marker=DisabledMarker.ALL,
                sector_code="*",
                population_group=PopulationGroup.ALL,
                population_status=PopulationStatus.AFFECTED,
                population=1_000_000,
                reference_period_start=datetime(2023, 1, 1),
                reference_period_end=datetime(2023, 1, 2),
            ),
        ],
        expected_constraint="max_age",
    )
