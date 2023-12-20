from hdx.database.views import build_view

from hapi_schema.db_food_security import view_params_food_security


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
