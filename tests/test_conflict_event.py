from datetime import datetime

from hdx.database import Database

from hapi_schema.db_conflict_event import (
    DBConflictEvent,
    view_params_conflict_event,
)


def test_conflict_event_view(run_view_test):
    """Check that national risk references other tables."""
    view_conflict_event = Database.prepare_view(
        view_params_conflict_event.__dict__
    )
    run_view_test(
        view=view_conflict_event,
        whereclause=(
            view_conflict_event.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_conflict_event.c.location_name == "Foolandia",
        ),
    )


def test_reference_period_constraint(run_constraints_test, base_parameters):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBConflictEvent(
                **base_parameters,
                **dict(
                    reference_period_start=datetime(2023, 1, 2),
                    reference_period_end=datetime(2023, 1, 1),
                ),
            )
        ],
        expected_constraint="reference_period",
    )
