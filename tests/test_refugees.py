from datetime import datetime

from hdx.database import Database

from hapi_schema.db_refugees import (
    DBRefugees,
    view_params_refugees,
)


def test_refugees_view(run_view_test):
    """Check that refugees view references other tables."""
    view_refugees = Database.prepare_view(view_params_refugees.__dict__)
    run_view_test(
        view=view_refugees,
        whereclause=(
            view_refugees.c.resource_hdx_id
            == "62ad6e55-5f5d-4494-854c-4110687e9e25",
            view_refugees.c.location_code == "FOO",
        ),
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBRefugees(
                resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
                admin2_ref=4,
                ipc_phase="1",
                ipc_type="current",
                population_in_phase=1_000,
                population_fraction_in_phase=1,
                reference_period_start=datetime(2023, 2, 1),
                reference_period_end=datetime(2023, 1, 1),
            )
        ],
        expected_constraint="reference_period",
    )


def test_population_in_phase_positive(run_constraints_test):
    """Check that the population value is positive"""
    run_constraints_test(
        new_rows=[
            DBRefugees(
                resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
                admin2_ref=4,
                ipc_phase="1",
                ipc_type="current",
                population_in_phase=-1,
                population_fraction_in_phase=1,
                reference_period_start=datetime(2023, 1, 1),
                reference_period_end=datetime(2023, 1, 2),
            )
        ],
        expected_constraint="population_in_phase",
    )
