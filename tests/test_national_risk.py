from datetime import datetime

from hdx.database.views import build_view

from hapi_schema.db_national_risk import (
    DBNationalRisk,
    view_params_national_risk,
)


def test_national_risk_view(run_view_test):
    """Check that national risk references other tables."""
    view_national_risk = build_view(view_params_national_risk.__dict__)
    run_view_test(
        view=view_national_risk,
        whereclause=(
            view_national_risk.c.id == 1,
            view_national_risk.c.dataset_hdx_id
            == "c3f001fa-b45b-464c-9460-1ca79fd39b40",
            view_national_risk.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_national_risk.c.resource_name == "resource-01.csv",
            view_national_risk.c.admin2_code == "FOO-XXX-XXX",
            view_national_risk.c.admin1_code == "FOO-XXX",
            view_national_risk.c.location_code == "FOO",
        ),
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBNationalRisk(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=1,
                risk_class=5,
                global_rank=4,
                overall_risk=8.1,
                hazard_exposure_risk=8.7,
                vulnerability_risk=8.5,
                coping_capacity_risk=7.1,
                meta_missing_indicators_pct=8,
                meta_avg_recentness_years=0.26,
                reference_period_start=datetime(2023, 1, 2),
                reference_period_end=datetime(2023, 1, 1),
                source_data="DATA,DATA,DATA",
            )
        ],
        expected_constraint="reference_period",
    )


def test_meta_avg_recentness_constraint(run_constraints_test):
    """Check that meta_avg_recentness_years is >= 0"""
    run_constraints_test(
        new_rows=[
            DBNationalRisk(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=1,
                risk_class=5,
                global_rank=4,
                overall_risk=8.1,
                hazard_exposure_risk=8.7,
                vulnerability_risk=8.5,
                coping_capacity_risk=7.1,
                meta_missing_indicators_pct=8,
                meta_avg_recentness_years=-100,
                reference_period_start=None,
                reference_period_end=None,
                source_data="DATA,DATA,DATA",
            )
        ],
        expected_constraint="meta_avg_recentness_years",
    )
