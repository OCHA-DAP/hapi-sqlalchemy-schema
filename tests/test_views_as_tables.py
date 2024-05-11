from hapi_schema.db_admin1 import view_params_admin1


def test_admin1_vat(run_indexes_test, run_columns_test, run_primary_keys_test):
    """Check that the admin1 view as table is correct - columns match, expected indexes present"""
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
