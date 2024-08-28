from datetime import datetime

from hdx.database import Database
from sqlalchemy.sql import null

from hapi_schema.db_idps import (
    DBIDPs,
    view_params_idps,
)
from hapi_schema.views import prepare_hapi_views


def test_idps_view(run_view_test):
    """Check idps view has all columns."""
    view_idps = Database.prepare_view(view_params_idps.__dict__)
    run_view_test(
        view=view_idps,
        whereclause=(
            view_idps.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_idps.c.appeal_code == "HFOO24",
            view_idps.c.location_ref == 1,
            view_idps.c.appeal_name == "Foolandia HRP 2024",
            view_idps.c.appeal_type == "HRP",
            view_idps.c.requirements_usd == 100000.0,
            view_idps.c.funding_usd == 50000.0,
            view_idps.c.funding_pct == 50.0,
            view_idps.c.location_code == "FOO",
            view_idps.c.location_name == "Foolandia",
        ),
    )


def test_idps_availability(run_view_test):
    view_availability = prepare_hapi_views()
    run_view_test(
        view=view_availability,
        whereclause=(
            view_availability.c.category == "coordination-context",
            view_availability.c.subcategory == "idps",
            view_availability.c.location_code == "FOO",
            view_availability.c.admin1_name == null(),
            view_availability.c.admin2_name == null(),
            view_availability.c.hapi_updated_date == datetime(2023, 6, 1),
        ),
    )


def test_reference_period_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBIDPs(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                appeal_code="HFOO24",
                location_ref=1,
                appeal_name="Foolandia HRP 2024",
                appeal_type="HRP",
                requirements_usd=100000.0,
                funding_usd=50000.0,
                funding_pct=50,
                reference_period_start=datetime(2025, 1, 1),
                reference_period_end=datetime(2024, 12, 31),
            ),
        ],
        expected_constraint="reference_period_constraint",
    )


def test_requirements_usd_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBIDPs(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                appeal_code="HFOO24",
                location_ref=1,
                appeal_name="Foolandia HRP 2024",
                appeal_type="HRP",
                requirements_usd=-100000.0,
                funding_usd=50000.0,
                funding_pct=50,
                reference_period_start=datetime(2024, 1, 1),
                reference_period_end=datetime(2024, 12, 31),
            ),
        ],
        expected_constraint="requirements_usd_constraint",
    )


def test_funding_usd_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBIDPs(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                appeal_code="HFOO24",
                location_ref=1,
                appeal_name="Foolandia HRP 2024",
                appeal_type="HRP",
                requirements_usd=100000.0,
                funding_usd=-50000.0,
                funding_pct=50,
                reference_period_start=datetime(2024, 1, 1),
                reference_period_end=datetime(2024, 12, 31),
            ),
        ],
        expected_constraint="funding_usd_constraint",
    )


def test_funding_pct_constraint(run_constraints_test):
    """Check that reference_period_end cannot be less than start"""
    run_constraints_test(
        new_rows=[
            DBIDPs(
                resource_hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
                appeal_code="HFOO24",
                location_ref=1,
                appeal_name="Foolandia HRP 2024",
                appeal_type="HRP",
                requirements_usd=100000.0,
                funding_usd=50000.0,
                funding_pct=-50,
                reference_period_start=datetime(2024, 1, 1),
                reference_period_end=datetime(2024, 12, 31),
            ),
        ],
        expected_constraint="funding_pct_constraint",
    )
