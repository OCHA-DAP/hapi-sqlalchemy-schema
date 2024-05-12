from hapi_schema.db_admin1 import view_params_admin1
from hapi_schema.db_admin2 import view_params_admin2
from hapi_schema.db_dataset import view_params_dataset
from hapi_schema.db_food_security import view_params_food_security


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


def test_food_security_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that food_security_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = [
        "admin2_ref",
        "ipc_type",
        "ipc_phase",
        "reference_period_start",
    ]
    expected_indexes = [
        "population_in_phase",
        "population_fraction_in_phase",
        "reference_period_end",
        "location_code",
        "location_name",
        "admin1_code",
        "admin1_name",
        "admin2_code",
        "admin2_name",
    ]
    run_columns_test(
        "food_security_vat", "food_security_view", view_params_food_security
    )
    run_indexes_test("food_security_vat", expected_indexes)
    run_primary_keys_test("food_security_vat", expected_primary_keys)
