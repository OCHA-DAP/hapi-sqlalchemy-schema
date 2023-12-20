from hdx.database.views import build_view

from hapi_schema.db_resource import view_params_resource


def test_resource_view(run_view_test):
    """Check that resource references dataset."""
    view_resource = build_view(view_params_resource.__dict__)
    run_view_test(
        view=view_resource,
        whereclause=(
            view_resource.c.id == 1,
            view_resource.c.dataset_hdx_id
            == "c3f001fa-b45b-464c-9460-1ca79fd39b40",
        ),
    )
