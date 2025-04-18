from datetime import datetime

from hdx.database import Database

from hapi_schema.db_food_security import (
    DBFoodSecurity,
    view_params_food_security,
)
from hapi_schema.views import prepare_hapi_views


def test_food_security_view(run_view_test):
    """Check that food security view references other tables."""
    view_food_security = Database.prepare_view(
        view_params_food_security.__dict__
    )
    run_view_test(
        view=view_food_security,
        whereclause=(
            view_food_security.c.resource_hdx_id
            == "62ad6e55-5f5d-4494-854c-4110687e9e25",
            view_food_security.c.admin2_code == "FOO-001-A",
            view_food_security.c.provider_admin1_name == "Provincia 01",
            view_food_security.c.provider_admin2_name == "Distrito A",
            view_food_security.c.admin1_code == "FOO-001",
            view_food_security.c.location_code == "FOO",
            view_food_security.c.admin_level == 2,
        ),
    )


def test_food_security_availability(run_view_test):
    view_availability = prepare_hapi_views()["data_availability"]
    run_view_test(
        view=view_availability,
        whereclause=(
            view_availability.c.category == "food-security-nutrition-poverty",
            view_availability.c.subcategory == "food-security",
            view_availability.c.location_code == "FOO",
            view_availability.c.admin1_name == "Province 01",
            view_availability.c.admin2_name == "District A",
            view_availability.c.admin_level == 2,
            view_availability.c.hapi_updated_date == datetime(2023, 8, 1),
        ),
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBFoodSecurity(
                resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
                admin2_ref=4,
                provider_admin1_name="Provincia 01",
                provider_admin2_name="Distrito A",
                ipc_phase="1",
                ipc_type="current",
                population_in_phase=1_000,
                population_fraction_in_phase=1,
                reference_period_start=datetime(2023, 2, 1),
                reference_period_end=datetime(2023, 1, 1),
            )
        ],
        expected_constraint="reference_period_constraint",
    )


def test_population_in_phase_positive(run_constraints_test):
    """Check that the population value is positive"""
    run_constraints_test(
        new_rows=[
            DBFoodSecurity(
                resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
                admin2_ref=4,
                provider_admin1_name="Provincia 01",
                provider_admin2_name="Distrito A",
                ipc_phase="1",
                ipc_type="current",
                population_in_phase=-1,
                population_fraction_in_phase=1,
                reference_period_start=datetime(2023, 1, 1),
                reference_period_end=datetime(2023, 1, 2),
            )
        ],
        expected_constraint="population_in_phase_constraint",
    )
