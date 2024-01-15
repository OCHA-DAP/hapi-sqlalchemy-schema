from hdx.database.views import build_view

from hapi_schema.db_national_risk import view_params_national_risk


def test_national_risk_view(run_view_test):
    """Check that national risk references other tables."""
    view_national_risk = build_view(view_params_national_risk.__dict__)
    run_view_test(
        view=view_national_risk,
        whereclause=(
            view_national_risk.c.id == 1,
            view_national_risk.c.dataset_hdx_id
            == "c3f001fa-b45b-464c-9460-1ca79fd39b40",
            view_national_risk.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_national_risk.c.location_code == "FOO",
        ),
    )
