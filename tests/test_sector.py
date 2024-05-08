from hdx.database import Database

from hapi_schema.db_sector import view_params_sector


def test_sector_view(run_view_test):
    """Check that sector view shows some columns."""
    view_sector = Database.prepare_view(view_params_sector.__dict__)
    run_view_test(
        view=view_sector,
        whereclause=(
            view_sector.c.code == "SHL",
            view_sector.c.name == "Emergency Shelter and NFI",
        ),
    )
