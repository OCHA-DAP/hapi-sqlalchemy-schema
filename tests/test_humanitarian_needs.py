from datetime import datetime

from hdx.database.views import build_view

from hapi_schema.db_humanitarian_needs import (
    DBHumanitarianNeeds,
    view_params_humanitarian_needs,
)


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
            view_humanitarian_needs.c.resource_name == "resource-01.csv",
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


def test_humanitarian_needs_vat(run_indexes_test, run_columns_test):
    """Check that the humanitarian_needs view as table is correct - columns match, expected indexes present"""
    expected_indexes = [
        "dataset_hdx_provider_stub",
        "dataset_hdx_provider_name",
        "resource_update_date",
        "hapi_updated_date",
        "hapi_replaced_date",
        "reference_period_start",
        "reference_period_end",
        "sector_name",
    ]
    run_columns_test(
        "humanitarian_needs_vat",
        "humanitarian_needs_view",
        view_params_humanitarian_needs,
    )
    run_indexes_test("humanitarian_needs_vat", expected_indexes)


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBHumanitarianNeeds(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                admin2_ref=1,
                gender_code=None,
                age_range_code=None,
                disabled_marker=None,
                sector_code=None,
                population_group_code=None,
                population_status_code="affected",
                population=1_000_000,
                reference_period_start=datetime(2023, 1, 2),
                reference_period_end=datetime(2023, 1, 1),
                source_data="DATA,DATA,DATA",
            )
        ],
        expected_constraint="reference_period",
    )
