from hdx.database import Database

from hapi_schema.db_resource import view_params_resource


def test_resource_view(run_view_test):
    """Check that resource references dataset."""
    view_resource = Database.prepare_view(view_params_resource.__dict__)
    run_view_test(
        view=view_resource,
        whereclause=(
            view_resource.c.hdx_id == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_resource.c.dataset_hdx_stub == "dataset01",
        ),
    )
