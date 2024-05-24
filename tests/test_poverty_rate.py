from datetime import datetime

from hdx.database import Database

from hapi_schema.db_poverty_rate import (
    DBPovertyRate,
    view_params_poverty_rate,
)


def test_poverty_rate_view(run_view_test):
    """Check that poverty_rate references other tables."""
    view_poverty_rate = Database.prepare_view(
        view_params_poverty_rate.__dict__
    )
    run_view_test(
        view=view_poverty_rate,
        whereclause=(
            view_poverty_rate.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_poverty_rate.c.location_name == "Foolandia",
            view_poverty_rate.c.admin1_name == "Province 01",
        ),
    )


def test_headcount_ratio_constraint(run_constraints_test):
    """Check that headcount ratio is between 0 and 100"""
    data = _sample_data()
    data["headcount_ratio"] = 101
    run_constraints_test(
        new_rows=[
            DBPovertyRate(**data),
        ],
        expected_constraint="headcount_ratio_constraint",
    )


def test_intensity_of_deprivation_constraint(run_constraints_test):
    """Check that intensity of deprivation is between 0 and 100"""
    data = _sample_data()
    data["intensity_of_deprivation"] = 101
    run_constraints_test(
        new_rows=[
            DBPovertyRate(**data),
        ],
        expected_constraint="intensity_of_deprivation_constraint",
    )


def test_vulnerable_to_poverty_constraint(run_constraints_test):
    """Check that vulnerable_to_poverty is between 0 and 100"""
    data = _sample_data()
    data["vulnerable_to_poverty"] = 101
    run_constraints_test(
        new_rows=[
            DBPovertyRate(**data),
        ],
        expected_constraint="vulnerable_to_poverty_constraint",
    )


def test_in_severe_poverty_constraint(run_constraints_test):
    """Check that in_severe_poverty is between 0 and 100"""
    data = _sample_data()
    data["in_severe_poverty"] = 101
    run_constraints_test(
        new_rows=[
            DBPovertyRate(**data),
        ],
        expected_constraint="in_severe_poverty_constraint",
    )


def test_mpi_product_constraint(run_constraints_test):
    """Check that MPI is the product of headcount and intensity"""
    data = _sample_data()
    data["mpi"] = 0.5
    run_constraints_test(
        new_rows=[
            DBPovertyRate(**data),
        ],
        expected_constraint="mpi_product_constraint",
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    data = _sample_data()
    data["reference_period_start"] = datetime(2025, 1, 1)
    run_constraints_test(
        new_rows=[
            DBPovertyRate(**data),
        ],
        expected_constraint="reference_period_constraint",
    )


def _sample_data():
    # return the whole record, then tests can change as needed
    return dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin1_ref=1,
        admin1_name="Province 02",
        mpi=0.617442,
        headcount_ratio=85.4,
        intensity_of_deprivation=72.3,
        vulnerable_to_poverty=10.5,
        in_severe_poverty=52.1,
        reference_period_start=datetime(2024, 1, 1),
        reference_period_end=datetime(2024, 12, 31),
    )
