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


def test_mpi_constraint(run_constraints_test):
    """Check that MPI is between 0.0 and 1.0"""
    data = _sample_data()
    data["multidimensional_poverty_index"] = 1.1
    run_constraints_test(
        new_rows=[
            DBPovertyRate(**data),
        ],
        expected_constraint="rate",
    )


def test_mpi_product_constraint(run_constraints_test):
    """Check that MPI is between 0.0 and 1.0"""
    data = _sample_data()
    data["multidimensional_poverty_index"] = 1.1
    run_constraints_test(
        new_rows=[
            DBPovertyRate(**data),
        ],
        expected_constraint="rate",
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    data = _sample_data()
    data["reference_period_start"] = datetime(2025, 1, 1)
    run_constraints_test(
        new_rows=[
            DBPovertyRate(**data),
        ],
        expected_constraint="reference_period",
    )


def _sample_data():
    # return the whole record, then tests can change as needed
    return dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin1_ref=1,
        admin1_name="Province 02",
        multidimensional_poverty_index=0.617442,
        headcount_ratio=85.4,
        intensity_of_deprivation=72.3,
        vulnerable_to_poverty=10.5,
        in_severe_poverty=52.1,
        population=10_000,
        reference_period_start=datetime(2024, 1, 1),
        reference_period_end=datetime(2024, 12, 31),
    )
