from hdx.database.views import build_view

from hapi_schema.db_ipc_phase import DBIpcPhase, view_params_ipc_phase


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
            view_ipc_phase.c.code == "1",
            view_ipc_phase.c.name == "Phase 1: None/Minimal",
            view_ipc_phase.c.description == phase1_description,
        ),
    )


def test_ipc_phase_code_constraint(run_constraints_test):
    """Check that ipc phase must be one of the allowed values"""
    # Random string
    run_constraints_test(
        new_rows=[
            DBIpcPhase(
                code="Nonsense", name="Nonsense", description="Nonsense"
            )
        ],
        expected_constraint="ipc_phase_code",
    )
