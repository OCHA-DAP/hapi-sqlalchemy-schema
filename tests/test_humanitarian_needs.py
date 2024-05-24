from datetime import datetime

import pytest
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
            view_humanitarian_needs.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
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


@pytest.fixture(scope="module")
def base_parameters():
    return dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=1,
        gender=Gender.ALL,
        age_range="-1-20",
        disabled_marker=DisabledMarker.ALL,
        sector_code="*",
        population_group=PopulationGroup.ALL,
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


def test_minage(run_constraints_test, base_parameters):
    """Check that the min_age value is positive, and NULL if
    age_range is all"""
    modified_params = {**base_parameters, **dict(age_range="5-10", min_age=-1)}
    run_constraints_test(
        new_rows=[
            DBHumanitarianNeeds(**modified_params),
        ],
        expected_constraint="min_age_constraint",
    )
    modified_params = {**base_parameters, **dict(age_range="all", min_age=10)}
    run_constraints_test(
        new_rows=[
            DBHumanitarianNeeds(**modified_params),
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
            DBHumanitarianNeeds(**modified_params),
        ],
        expected_constraint="max_age_constraint",
    )
    modified_params = {
        **base_parameters,
        **dict(age_range="unknown", min_age=None, max_age=10),
    }
    run_constraints_test(
        new_rows=[
            DBHumanitarianNeeds(**modified_params),
        ],
        expected_constraint="max_age_constraint",
    )
