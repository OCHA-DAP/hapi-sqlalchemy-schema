from hapi_schema.db_admin1 import view_params_admin1
from hapi_schema.db_admin2 import view_params_admin2
from hapi_schema.db_dataset import view_params_dataset


def test_admin1_vat(run_indexes_test, run_columns_test, run_primary_keys_test):
    """Check that the admin1_vat as table is correct - columns match, expected indexes present"""
    expected_primary_keys = ["id"]
    expected_indexes = [
        "code",
        "name",
        "reference_period_start",
        "reference_period_end",
        "location_code",
        "location_name",
    ]
    run_columns_test("admin1_vat", "admin1_view", view_params_admin1)
    run_indexes_test("admin1_vat", expected_indexes)
    run_primary_keys_test("admin1_vat", expected_primary_keys)


def test_admin2_vat(run_indexes_test, run_columns_test, run_primary_keys_test):
    """Check that admin2_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["id"]
    expected_indexes = [
        "code",
        "name",
        "reference_period_start",
        "reference_period_end",
        "location_code",
        "location_name",
    ]
    run_columns_test("admin2_vat", "admin2_view", view_params_admin2)
    run_indexes_test("admin2_vat", expected_indexes)
    run_primary_keys_test("admin2_vat", expected_primary_keys)


def test_dataset_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that dataset_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["hdx_id"]
    expected_indexes = ["hdx_stub", "hdx_provider_stub", "hdx_provider_name"]
    run_columns_test("dataset_vat", "dataset_view", view_params_dataset)
    run_indexes_test("dataset_vat", expected_indexes)
    run_primary_keys_test("dataset_vat", expected_primary_keys)
