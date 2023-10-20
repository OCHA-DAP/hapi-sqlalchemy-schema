from hdx.database.views import build_view

from hapi_schema.db_admin1 import view_params_admin1
from hapi_schema.db_admin2 import view_params_admin2
from hapi_schema.db_age_range import view_params_age_range
from hapi_schema.db_dataset import view_params_dataset
from hapi_schema.db_food_security import view_params_food_security
from hapi_schema.db_gender import view_params_gender
from hapi_schema.db_ipc_phase import view_params_ipc_phase
from hapi_schema.db_ipc_type import view_params_ipc_type
from hapi_schema.db_location import view_params_location
from hapi_schema.db_operational_presence import (
    view_params_operational_presence,
)
from hapi_schema.db_org import view_params_org
from hapi_schema.db_org_type import view_params_org_type
from hapi_schema.db_population import view_params_population
from hapi_schema.db_resource import view_params_resource
from hapi_schema.db_sector import view_params_sector


def test_admin1_view(run_view_test):
    """Check that admin1 view references location."""
    view_admin1 = build_view(view_params_admin1.__dict__)
    run_view_test(
        view=view_admin1,
        whereclause=(
            view_admin1.c.id == 1,
            view_admin1.c.location_code == "FOO",
        ),
    )


def test_admin2_view(run_view_test):
    """Check that admin2 view references admin1 and location."""
    view_admin2 = build_view(view_params_admin2.__dict__)
    run_view_test(
        view=view_admin2,
        whereclause=(
            view_admin2.c.id == 1,
            view_admin2.c.admin1_code == "FOO-XXX",
            view_admin2.c.location_code == "FOO",
        ),
    )


def test_age_range_view(run_view_test):
    """Check that age range shows code and numbers."""
    view_age_range = build_view(view_params_age_range.__dict__)
    run_view_test(
        view=view_age_range,
        whereclause=(
            view_age_range.c.code == "0-4",
            view_age_range.c.age_min == 0,
            view_age_range.c.age_max == 4,
        ),
    )


def test_dataset_view(run_view_test):
    """Check that dataset view has most columns."""
    view_dataset = build_view(view_params_dataset.__dict__)
    run_view_test(
        view=view_dataset,
        whereclause=(
            view_dataset.c.id == 1,
            view_dataset.c.hdx_stub == "dataset01",
            view_dataset.c.title == "Dataset #1",
            view_dataset.c.hdx_provider_stub == "provider01",
            view_dataset.c.hdx_provider_name == "Provider #1",
        ),
    )


def test_food_security_view(run_view_test):
    """Check that food security view references other tables."""
    view_food_security = build_view(view_params_food_security.__dict__)
    run_view_test(
        view=view_food_security,
        whereclause=(
            view_food_security.c.id == 3,
            view_food_security.c.dataset_hdx_id
            == "7cf3cec8-dbbc-4c96-9762-1464cd0bff75",
            view_food_security.c.resource_hdx_id
            == "62ad6e55-5f5d-4494-854c-4110687e9e25",
            view_food_security.c.ipc_phase_name == "Phase 3: Crisis",
            view_food_security.c.admin2_code == "FOO-001-A",
            view_food_security.c.admin1_code == "FOO-001",
            view_food_security.c.location_code == "FOO",
        ),
    )


def test_gender_view(run_view_test):
    """Check gender view has all columns."""
    view_gender = build_view(view_params_gender.__dict__)
    run_view_test(
        view=view_gender,
        whereclause=(
            view_gender.c.code == "f",
            view_gender.c.description == "female",
        ),
    )


def test_ipc_phase_view(run_view_test):
    """Check IPC phase view has all columns."""
    phase1_description = (
        "Households are able to meet essential food and non-food "
        "needs without engaging in atypical and unsustainable "
        "strategies to access food and income."
    )
    view_ipc_phase = build_view(view_params_ipc_phase.__dict__)
    run_view_test(
        view=view_ipc_phase,
        whereclause=(
            view_ipc_phase.c.code == 1,
            view_ipc_phase.c.name == "Phase 1: None/Minimal",
            view_ipc_phase.c.description == phase1_description,
        ),
    )


def test_ipc_type_view(run_view_test):
    """Check IPC type view has all columns."""

    view_ipc_type = build_view(view_params_ipc_type.__dict__)
    run_view_test(
        view=view_ipc_type,
        whereclause=(
            view_ipc_type.c.code == "current",
            view_ipc_type.c.description == "Food insecurity that is "
            "occurring in the current "
            "analysis period.",
        ),
    )


def test_location_view(run_view_test):
    """Check that location view has some columns."""
    view_location = build_view(view_params_location.__dict__)
    run_view_test(
        view=view_location,
        whereclause=(
            view_location.c.id == 1,
            view_location.c.code == "FOO",
            view_location.c.name == "Foolandia",
        ),
    )


def test_operational_presence_view(run_view_test):
    """Check that OP view has all references."""
    view_operational_presence = build_view(
        view_params_operational_presence.__dict__
    )
    run_view_test(
        view=view_operational_presence,
        whereclause=(
            view_operational_presence.c.id == 5,
            view_operational_presence.c.dataset_hdx_id
            == "c3f001fa-b45b-464c-9460-1ca79fd39b40",
            view_operational_presence.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_operational_presence.c.admin2_code == "FOO-XXX-XXX",
            view_operational_presence.c.admin1_code == "FOO-XXX",
            view_operational_presence.c.location_code == "FOO",
            view_operational_presence.c.org_type_description
            == "International NGO",
            view_operational_presence.c.org_acronym == "ORG02",
        ),
    )


def test_org_view(run_view_test):
    """Check that org view references org type."""
    view_org = build_view(view_params_org.__dict__)
    run_view_test(
        view=view_org,
        whereclause=(
            view_org.c.id == 1,
            view_org.c.org_type_code == "433",
            view_org.c.org_type_description == "Donor",
        ),
    )


def test_org_type_view(run_view_test):
    """Check that org type has all fields."""
    dict(code="433", description="Donor"),
    view_org_type = build_view(view_params_org_type.__dict__)
    run_view_test(
        view=view_org_type,
        whereclause=(
            view_org_type.c.code == "433",
            view_org_type.c.description == "Donor",
        ),
    )


def test_population_view(run_view_test):
    """Check that population references other tables."""
    view_population = build_view(view_params_population.__dict__)
    run_view_test(
        view=view_population,
        whereclause=(
            view_population.c.id == 3,
            view_population.c.dataset_hdx_id
            == "c3f001fa-b45b-464c-9460-1ca79fd39b40",
            view_population.c.resource_hdx_id
            == "90deb235-1bf5-4bae-b231-3393222c2d01",
            view_population.c.gender_description == "female",
            view_population.c.admin2_code == "FOO-001-XXX",
            view_population.c.admin1_code == "FOO-001",
            view_population.c.location_code == "FOO",
        ),
    )


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


def test_sector_view(run_view_test):
    """Check that sector view shows some columns."""
    view_sector = build_view(view_params_sector.__dict__)
    run_view_test(
        view=view_sector,
        whereclause=(
            view_sector.c.code == "SHL",
            view_sector.c.name == "Emergency Shelter and NFI",
        ),
    )
