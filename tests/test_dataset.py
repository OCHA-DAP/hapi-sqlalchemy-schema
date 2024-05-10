from hdx.database import Database

from hapi_schema.db_dataset import view_params_dataset


def test_dataset_view(run_view_test):
    """Check that dataset view has most columns."""
    view_dataset = Database.prepare_view(view_params_dataset.__dict__)
    run_view_test(
        view=view_dataset,
        whereclause=(
            view_dataset.c.hdx_id == "c3f001fa-b45b-464c-9460-1ca79fd39b40",
            view_dataset.c.hdx_stub == "dataset01",
            view_dataset.c.title == "Dataset #1",
            view_dataset.c.hdx_provider_stub == "provider01",
            view_dataset.c.hdx_provider_name == "Provider #1",
        ),
    )


def test_dataset_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that the view as table is correct - columns match, expected indexes present"""
    expected_primary_keys = ["hdx_id"]
    expected_indexes = ["hdx_stub", "hdx_provider_stub", "hdx_provider_name"]
    run_columns_test("dataset_vat", "dataset_view", view_params_dataset)
    run_indexes_test("dataset_vat", expected_indexes)
    run_primary_keys_test("dataset_vat", expected_primary_keys)
