from hapi_schema.db_admin1 import view_params_admin1
from hapi_schema.db_admin2 import view_params_admin2
from hapi_schema.db_conflict_event import view_params_conflict_event
from hapi_schema.db_currency import view_params_currency
from hapi_schema.db_dataset import view_params_dataset
from hapi_schema.db_food_price import view_params_food_price
from hapi_schema.db_food_security import view_params_food_security
from hapi_schema.db_funding import view_params_funding
from hapi_schema.db_humanitarian_needs import view_params_humanitarian_needs
from hapi_schema.db_location import view_params_location
from hapi_schema.db_national_risk import view_params_national_risk
from hapi_schema.db_operational_presence import (
    view_params_operational_presence,
)
from hapi_schema.db_org import view_params_org
from hapi_schema.db_org_type import view_params_org_type
from hapi_schema.db_patch import view_params_patch
from hapi_schema.db_population import view_params_population
from hapi_schema.db_poverty_rate import view_params_poverty_rate
from hapi_schema.db_refugees import view_params_refugees
from hapi_schema.db_resource import view_params_resource
from hapi_schema.db_sector import view_params_sector
from hapi_schema.db_wfp_commodity import view_params_wfp_commodity
from hapi_schema.db_wfp_market import view_params_wfp_market


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


def test_conflict_event_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that conflict_event_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = [
        "admin2_ref",
        "event_type",
        "reference_period_start",
    ]
    expected_indexes = [
        "events",
        "fatalities",
        "reference_period_end",
        "location_code",
        "location_name",
        "admin1_code",
        "admin1_name",
        "admin2_code",
        "admin2_name",
    ]
    run_columns_test(
        "conflict_event_vat", "conflict_event_view", view_params_conflict_event
    )
    run_indexes_test("conflict_event_vat", expected_indexes)
    run_primary_keys_test("conflict_event_vat", expected_primary_keys)


def test_currency_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that currency_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["code"]
    expected_indexes = ["name"]
    run_columns_test("currency_vat", "currency_view", view_params_currency)
    run_indexes_test("currency_vat", expected_indexes)
    run_primary_keys_test("currency_vat", expected_primary_keys)


def test_dataset_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that dataset_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["hdx_id"]
    expected_indexes = ["hdx_stub", "hdx_provider_stub", "hdx_provider_name"]
    run_columns_test("dataset_vat", "dataset_view", view_params_dataset)
    run_indexes_test("dataset_vat", expected_indexes)
    run_primary_keys_test("dataset_vat", expected_primary_keys)


def test_food_price_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that food_price_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = [
        "market_code",
        "commodity_code",
        "unit",
        "price_flag",
        "price_type",
        "reference_period_start",
    ]
    expected_indexes = [
        "currency_code",
        "commodity_name",
        "market_name",
        "lat",
        "lon",
        "reference_period_end",
        "location_code",
        "location_name",
        "admin1_code",
        "admin1_name",
        "admin2_code",
        "admin2_name",
    ]
    run_columns_test(
        "food_price_vat", "food_price_view", view_params_food_price
    )
    run_indexes_test("food_price_vat", expected_indexes)
    run_primary_keys_test("food_price_vat", expected_primary_keys)


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


def test_funding_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that funding_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["appeal_code", "location_ref"]
    expected_indexes = [
        "requirements_usd",
        "funding_usd",
        "funding_pct",
        "reference_period_start",
        "location_code",
        "location_name",
    ]
    run_columns_test("funding_vat", "funding_view", view_params_funding)
    run_indexes_test("funding_vat", expected_indexes)
    run_primary_keys_test("funding_vat", expected_primary_keys)


def test_humanitarian_needs_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that humanitarian_needs_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = [
        "admin2_ref",
        "gender",
        "age_range",
        "sector_code",
        "population_group",
        "population_status",
        "disabled_marker",
        "reference_period_start",
    ]
    expected_indexes = [
        "min_age",
        "max_age",
        "reference_period_end",
        "location_code",
        "location_name",
        "admin1_code",
        "admin1_name",
        "admin2_code",
        "admin2_name",
    ]
    run_columns_test(
        "humanitarian_needs_vat",
        "humanitarian_needs_view",
        view_params_humanitarian_needs,
    )
    run_indexes_test("humanitarian_needs_vat", expected_indexes)
    run_primary_keys_test("humanitarian_needs_vat", expected_primary_keys)


def test_location_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that location_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["id"]
    expected_indexes = [
        "code",
        "name",
        "reference_period_start",
        "reference_period_end",
    ]
    run_columns_test("location_vat", "location_view", view_params_location)
    run_indexes_test("location_vat", expected_indexes)
    run_primary_keys_test("location_vat", expected_primary_keys)


def test_national_risk_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that national_risk_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["location_ref", "reference_period_start"]
    expected_indexes = [
        "reference_period_end",
        "location_code",
        "location_name",
    ]
    run_columns_test(
        "national_risk_vat", "national_risk_view", view_params_national_risk
    )
    run_indexes_test("national_risk_vat", expected_indexes)
    run_primary_keys_test("national_risk_vat", expected_primary_keys)


def test_operational_presence_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that operational_presence_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = [
        "admin2_ref",
        "org_acronym",
        "org_name",
        "sector_code",
        "reference_period_start",
    ]
    expected_indexes = [
        "org_type_description",
        "reference_period_end",
        "location_code",
        "location_name",
        "admin1_code",
        "admin1_name",
        "admin2_code",
        "admin2_name",
    ]
    run_columns_test(
        "operational_presence_vat",
        "operational_presence_view",
        view_params_operational_presence,
    )
    run_indexes_test("operational_presence_vat", expected_indexes)
    run_primary_keys_test("operational_presence_vat", expected_primary_keys)


def test_org_type_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that org_type_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["code"]
    expected_indexes = ["description"]
    run_columns_test("org_type_vat", "org_type_view", view_params_org_type)
    run_indexes_test("org_type_vat", expected_indexes)
    run_primary_keys_test("org_type_vat", expected_primary_keys)


def test_org_vat(run_indexes_test, run_columns_test, run_primary_keys_test):
    """Check that org_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["acronym", "name"]
    expected_indexes = ["org_type_code", "org_type_description"]
    run_columns_test("org_vat", "org_view", view_params_org)
    run_indexes_test("org_vat", expected_indexes)
    run_primary_keys_test("org_vat", expected_primary_keys)


def test_patch_vat(run_indexes_test, run_columns_test, run_primary_keys_test):
    """Check that patch_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["id"]
    expected_indexes = [
        "patch_sequence_number",
        "patch_path",
        "state",
        "execution_date",
    ]
    run_columns_test("patch_vat", "patch_view", view_params_patch)
    run_indexes_test("patch_vat", expected_indexes)
    run_primary_keys_test("patch_vat", expected_primary_keys)


def test_population_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that population_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["admin2_ref", "gender", "age_range"]
    expected_indexes = [
        "min_age",
        "max_age",
        "population",
        "reference_period_start",
        "reference_period_end",
        "location_code",
        "location_name",
        "admin1_code",
        "admin1_name",
        "admin2_code",
        "admin2_name",
    ]
    run_columns_test(
        "population_vat", "population_view", view_params_population
    )
    run_indexes_test("population_vat", expected_indexes)
    run_primary_keys_test("population_vat", expected_primary_keys)


def test_poverty_rate_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that poverty_rate_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = [
        "admin1_ref",
        "admin1_name",
        "reference_period_start",
    ]
    expected_indexes = [
        "reference_period_end",
        "location_ref",
        "location_code",
        "location_name",
        "admin1_name",
    ]
    run_columns_test(
        "poverty_rate_vat", "poverty_rate_view", view_params_poverty_rate
    )
    run_indexes_test("poverty_rate_vat", expected_indexes)
    run_primary_keys_test("poverty_rate_vat", expected_primary_keys)


def test_refugees_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that refugees_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = [
        "origin_location_ref",
        "asylum_location_ref",
        "population_group",
        "gender",
        "age_range",
        "reference_period_start",
    ]
    expected_indexes = [
        "min_age",
        "max_age",
        "population",
        "reference_period_end",
        "origin_location_code",
        "origin_location_name",
        "asylum_location_code",
        "asylum_location_name",
    ]
    run_columns_test("refugees_vat", "refugees_view", view_params_refugees)
    run_indexes_test("refugees_vat", expected_indexes)
    run_primary_keys_test("refugees_vat", expected_primary_keys)


def test_resource_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that resource_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["hdx_id"]
    expected_indexes = [
        "dataset_hdx_stub",
        "dataset_hdx_provider_stub",
        "dataset_hdx_provider_name",
    ]
    run_columns_test("resource_vat", "resource_view", view_params_resource)
    run_indexes_test("resource_vat", expected_indexes)
    run_primary_keys_test("resource_vat", expected_primary_keys)


def test_sector_vat(run_indexes_test, run_columns_test, run_primary_keys_test):
    """Check that sector_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["code"]
    expected_indexes = ["name"]
    run_columns_test("sector_vat", "sector_view", view_params_sector)
    run_indexes_test("sector_vat", expected_indexes)
    run_primary_keys_test("sector_vat", expected_primary_keys)


def test_wfp_commodity_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that wfp_commodity_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["code"]
    expected_indexes = ["category", "name"]
    run_columns_test(
        "wfp_commodity_vat", "wfp_commodity_view", view_params_wfp_commodity
    )
    run_indexes_test("wfp_commodity_vat", expected_indexes)
    run_primary_keys_test("wfp_commodity_vat", expected_primary_keys)


def test_wfp_market_vat(
    run_indexes_test, run_columns_test, run_primary_keys_test
):
    """Check that wfp_market_vat is correct - columns match, expected indexes present"""
    expected_primary_keys = ["code"]
    expected_indexes = [
        "name",
        "lat",
        "lon",
        "lat",
        "lon",
        "location_code",
        "location_name",
        "admin1_code",
        "admin1_name",
        "admin2_code",
        "admin2_name",
    ]
    run_columns_test(
        "wfp_market_vat", "wfp_market_view", view_params_wfp_market
    )
    run_indexes_test("wfp_market_vat", expected_indexes)
    run_primary_keys_test("wfp_market_vat", expected_primary_keys)
