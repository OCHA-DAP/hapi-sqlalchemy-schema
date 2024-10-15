from datetime import datetime

from hdx.database import Database

from hapi_schema.db_operational_presence import (
    DBOperationalPresence,
    view_params_operational_presence,
)
from hapi_schema.views import prepare_hapi_views


def test_operational_presence_view(run_view_test):
    """Check that OP view has all references."""
    view_operational_presence = Database.prepare_view(
        view_params_operational_presence.__dict__
    )
    run_view_test(
        view=view_operational_presence,
        whereclause=(
            view_operational_presence.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_operational_presence.c.provider_admin1_name == "Provincia 01",
            view_operational_presence.c.provider_admin2_name == "Distrito A",
            view_operational_presence.c.admin2_code == "FOO-XXX-XXX",
            view_operational_presence.c.admin1_code == "FOO-XXX",
            view_operational_presence.c.location_code == "FOO",
            view_operational_presence.c.org_acronym == "ORG02",
            view_operational_presence.c.org_type_code == "437",
            view_operational_presence.c.org_type_description
            == "International NGO",
            view_operational_presence.c.sector_name
            == "Water Sanitation Hygiene",
        ),
    )


def test_operational_presence_availability(run_view_test):
    view_availability = prepare_hapi_views()[-1]
    run_view_test(
        view=view_availability,
        whereclause=(
            view_availability.c.category == "coordination-context",
            view_availability.c.subcategory == "operational-presence",
            view_availability.c.location_code == "FOO",
            view_availability.c.admin1_name == "Province 01",
            view_availability.c.admin2_name == "District A",
            view_availability.c.hapi_updated_date == datetime(2023, 6, 1),
        ),
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBOperationalPresence(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=2,
                provider_admin1_name="Provincia 01",
                provider_admin2_name="Distrito A",
                org_acronym="ORG01",
                org_name="Organisation 1",
                sector_code="SHL",
                reference_period_start=datetime(2023, 1, 2),
                reference_period_end=datetime(2023, 1, 1),
            )
        ],
        expected_constraint="reference_period_constraint",
    )
