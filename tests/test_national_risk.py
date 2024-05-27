from datetime import datetime

import pytest
from hdx.database import Database

from hapi_schema.db_national_risk import (
    DBNationalRisk,
    view_params_national_risk,
)


def test_national_risk_view(run_view_test):
    """Check that national risk references other tables."""
    view_national_risk = Database.prepare_view(
        view_params_national_risk.__dict__
    )
    run_view_test(
        view=view_national_risk,
        whereclause=(
            view_national_risk.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_national_risk.c.location_name == "Foolandia",
        ),
    )


@pytest.fixture
def base_parameters():
    return dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        location_ref=1,
        risk_class="5",
        global_rank=4,
        overall_risk=8.1,
        hazard_exposure_risk=8.7,
        vulnerability_risk=8.5,
        coping_capacity_risk=7.1,
        meta_missing_indicators_pct=8,
        meta_avg_recentness_years=0.26,
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
        new_rows=[
            DBNationalRisk(
                **modified_params,
            )
        ],
        expected_constraint="reference_period_constraint",
    )


def test_overall_risk_constraint(run_constraints_test, base_parameters):
    """Check that overall risk is >= 0 and <= 10"""
    modified_params = {**base_parameters, "overall_risk": -1}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="overall_risk_constraint",
    )
    modified_params = {**base_parameters, "overall_risk": 11}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="overall_risk_constraint",
    )


def test_hazard_exposure_constraint(run_constraints_test, base_parameters):
    """Check that hazard exposure is >= 0 and <= 10"""
    modified_params = {**base_parameters, "hazard_exposure_risk": -1}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="hazard_exposure_risk",
    )
    modified_params = {**base_parameters, "hazard_exposure_risk": 11}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="hazard_exposure_risk",
    )


def test_vulnerability_constraint(run_constraints_test, base_parameters):
    """Check that vulnerability is >= 0 and <= 10"""
    modified_params = {**base_parameters, "vulnerability_risk": -1}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="vulnerability_risk",
    )
    modified_params = {**base_parameters, "vulnerability_risk": 11}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="vulnerability_risk",
    )


def test_coping_capacity_constraint(run_constraints_test, base_parameters):
    """Check that coping capacity is >= 0 and <= 10"""
    modified_params = {**base_parameters, "coping_capacity_risk": -1}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="coping_capacity_risk",
    )
    modified_params = {**base_parameters, "coping_capacity_risk": 11}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="coping_capacity_risk",
    )


def test_coping_global_rank_constraint(run_constraints_test, base_parameters):
    """Check that global_rank is >= 1 and <= 250"""
    modified_params = {**base_parameters, "global_rank": 0}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="global_rank",
    )
    modified_params = {**base_parameters, "global_rank": 251}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="global_rank",
    )


def test_meta_avg_recentness_constraint(run_constraints_test, base_parameters):
    """Check that meta_avg_recentness_years is >= 0"""
    modified_params = {**base_parameters, "meta_avg_recentness_years": -1}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="meta_avg_recentness_years",
    )


def test_meta_missing_indicators_pct(run_constraints_test, base_parameters):
    """Check that meta_avg_recentness_years is >= 0 and <= 1"""
    modified_params = {**base_parameters, "meta_missing_indicators_pct": -1}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="meta_missing_indicators_pct",
    )
    modified_params = {**base_parameters, "meta_missing_indicators_pct": 101}
    run_constraints_test(
        new_rows=[DBNationalRisk(**modified_params)],
        expected_constraint="meta_missing_indicators_pct",
    )
