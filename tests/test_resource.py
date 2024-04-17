from datetime import datetime

from hdx.database.views import build_view

from hapi_schema.db_resource import DBResource, view_params_resource


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


def test_hapi_date_constraint(run_constraints_test):
    """Check that hapi_replaced_date cannot be less than hapi_updated_date"""
    run_constraints_test(
        new_rows=[
            DBResource(
                dataset_ref=2,
                hdx_id="9d9e07c9-a758-43bd-87dc-5cdd3b3f7e9f",
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
            dataset_ref=2,
            hdx_id="9d9e07c9-a758-43bd-87dc-5cdd3b3f7e9f",
            name="resource-04.csv",
            format="csv",
            update_date=datetime(2023, 1, 1),
            download_url="https://data.humdata.org/dataset/7cf3cec8-dbbc-4c96-9762-1464cd0bff75/resource/9d9e07c9-a758-43bd-87dc-5cdd3b3f7e9f/download/resource-04.csv",
            is_hxl=True,
            hapi_updated_date=datetime(2023, 8, 1),
            hapi_replaced_date=None,
        ),
    )
