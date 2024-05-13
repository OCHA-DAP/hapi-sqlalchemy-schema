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


def test_population_constraint(run_constraints_test):
    """Check that population cannot be negative"""
    data = _sample_data()
    data["population"] = -1
    run_constraints_test(
        new_rows=[
            DBPovertyRate(**data),
        ],
        expected_constraint="population",
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


# Util functions


def _sample_data():
    # return the whole record, then tests can change as needed
    return dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin1_ref=1,
        classification="vulnerable",
        population=1000000,
        reference_period_start=datetime(2024, 1, 1),
        reference_period_end=datetime(2024, 12, 31),
    )
