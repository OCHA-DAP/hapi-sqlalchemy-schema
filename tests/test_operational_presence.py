from datetime import datetime

from hdx.database.views import build_view

from hapi_schema.db_operational_presence import (
    DBOperationalPresence,
    view_params_operational_presence,
)


def test_operational_presence_view(run_view_test):
    """Check that OP view has all references."""
    view_operational_presence = build_view(
        view_params_operational_presence.__dict__
    )
    run_view_test(
        view=view_operational_presence,
        whereclause=(
            view_operational_presence.c.id == 5,
            view_operational_presence.c.dataset_hdx_id
            == "c3f001fa-b45b-464c-9460-1ca79fd39b40",
            view_operational_presence.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_operational_presence.c.admin2_code == "FOO-XXX-XXX",
            view_operational_presence.c.admin1_code == "FOO-XXX",
            view_operational_presence.c.location_code == "FOO",
            view_operational_presence.c.org_type_description
            == "International NGO",
            view_operational_presence.c.org_acronym == "ORG02",
            view_operational_presence.c.sector_name
            == "Water Sanitation Hygiene",
        ),
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBOperationalPresence(
                resource_ref=1,
                admin2_ref=2,
                org_ident="611c255706bfb8370827cba2a149a45f",
                sector_code="SHL",
                reference_period_start=datetime(2023, 1, 2),
                reference_period_end=datetime(2023, 1, 1),
                source_data="DATA,DATA,DATA",
            )
        ],
        expected_constraint="reference_period",
    )
