from hdx.database.views import build_view

from hapi_schema.db_operational_presence import (
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
