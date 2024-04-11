from hdx.database.views import build_view

from hapi_schema.db_humanitarian_needs import view_params_humanitarian_needs


def test_humanitarian_needs_view(run_view_test):
    """Check that humanitarian needs references other tables."""
    view_humanitarian_needs = build_view(
        view_params_humanitarian_needs.__dict__
    )
    run_view_test(
        view=view_humanitarian_needs,
        whereclause=(
            view_humanitarian_needs.c.id == 3,
            view_humanitarian_needs.c.dataset_hdx_id
            == "c3f001fa-b45b-464c-9460-1ca79fd39b40",
            view_humanitarian_needs.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_humanitarian_needs.c.admin2_code == "FOO-001-XXX",
            view_humanitarian_needs.c.admin1_code == "FOO-001",
            view_humanitarian_needs.c.location_code == "FOO",
            view_humanitarian_needs.c.population_status_code == "inneed",
            view_humanitarian_needs.c.population_group_code == "idps",
            view_humanitarian_needs.c.sector_name
            == "Water Sanitation Hygiene",
            view_humanitarian_needs.c.gender_code == "f",
            view_humanitarian_needs.c.disabled_marker == True,  # noqa: E712
        ),
    )
