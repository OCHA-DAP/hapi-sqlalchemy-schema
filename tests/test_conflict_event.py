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
            view_conflict_event.c.admin1_name == "Province 01",
            view_conflict_event.c.admin2_name == "District A",
        ),
    )


def _sample_data():
    # KISS principle (return the whole record, then change as needed)
    return dict(
        resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        admin2_ref=4,
        event_type="political_violence",
        events=10,
        fatalities=2,
        reference_period_start=datetime(2024, 1, 1),
        reference_period_end=datetime(2024, 1, 31),
    )


def test_events_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    data = _sample_data()
    data["events"] = -1
    run_constraints_test(
        new_rows=[
            DBConflictEvent(**data),
        ],
        expected_constraint="events_constraint",
    )


def test_fatalities_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    data = _sample_data()
    data["fatalities"] = -1
    run_constraints_test(
        new_rows=[
            DBConflictEvent(**data),
        ],
        expected_constraint="fatalities_constraint",
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    data = _sample_data()
    data["reference_period_start"] = datetime(2025, 1, 1)
    run_constraints_test(
        new_rows=[
            DBConflictEvent(**data),
        ],
        expected_constraint="reference_period_constraint",
    )
