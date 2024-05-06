from datetime import datetime

from hdx.database.views import build_view

from hapi_schema.db_resource import DBResource, view_params_resource


def test_resource_view(run_view_test):
    """Check that resource references dataset."""
    view_resource = build_view(view_params_resource.__dict__)
    run_view_test(
        view=view_resource,
        whereclause=(
            view_resource.c.hdx_id == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_resource.c.dataset_hdx_stub == "dataset01",
        ),
    )


def test_resource_vat(run_indexes_test, run_columns_test):
    """Check that the resource view as table is correct - columns match, expected indexes present"""
    expected_indexes = [
        "dataset_hdx_provider_stub",
        "dataset_hdx_provider_name",
        "hapi_updated_date",
        "hapi_replaced_date",
    ]
    run_columns_test(
        "resource_vat",
        "resource_view",
        view_params_resource,
    )
    run_indexes_test("resource_vat", expected_indexes)


def test_hapi_date_constraint(run_constraints_test):
    """Check that hapi_replaced_date cannot be less than hapi_updated_date"""
    run_constraints_test(
        new_rows=[
            DBResource(
                hdx_id="9d9e07c9-a758-43bd-87dc-5cdd3b3f7e9f",
                dataset_hdx_id="7cf3cec8-dbbc-4c96-9762-1464cd0bff75",
                name="resource-04.csv",
                format="csv",
                update_date=datetime(2023, 1, 1),
                download_url="https://data.humdata.org/dataset/7cf3cec8-dbbc-4c96-9762-1464cd0bff75/resource/9d9e07c9-a758-43bd-87dc-5cdd3b3f7e9f/download/resource-04.csv",
                is_hxl=True,
                hapi_updated_date=datetime(2023, 1, 2),
                hapi_replaced_date=datetime(2023, 1, 1),
            )
        ],
        expected_constraint="hapi_dates",
    )

    (
        dict(
            hdx_id="9d9e07c9-a758-43bd-87dc-5cdd3b3f7e9f",
            dataset_hdx_id="7cf3cec8-dbbc-4c96-9762-1464cd0bff75",
            name="resource-04.csv",
            format="csv",
            update_date=datetime(2023, 1, 1),
            download_url="https://data.humdata.org/dataset/7cf3cec8-dbbc-4c96-9762-1464cd0bff75/resource/9d9e07c9-a758-43bd-87dc-5cdd3b3f7e9f/download/resource-04.csv",
            is_hxl=True,
            hapi_updated_date=datetime(2023, 8, 1),
            hapi_replaced_date=None,
        ),
    )
