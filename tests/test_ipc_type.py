from hdx.database.views import build_view

from hapi_schema.db_ipc_type import DBIpcType, view_params_ipc_type


def test_ipc_type_view(run_view_test):
    """Check IPC type view has all columns."""

    view_ipc_type = build_view(view_params_ipc_type.__dict__)
    run_view_test(
        view=view_ipc_type,
        whereclause=(
            view_ipc_type.c.code == "current",
            view_ipc_type.c.description == "Food insecurity that is "
            "occurring in the current analysis period.",
        ),
    )


def test_ipc_phase_type_constraint(run_constraints_test):
    """Check that ipc type must be one of the allowed values"""
    # Random string
    run_constraints_test(
        new_rows=[DBIpcType(code="Nonsense", description="Nonsense")],
        expected_constraint="ipc_phase_type",
    )
