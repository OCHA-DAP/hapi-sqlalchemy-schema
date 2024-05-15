from hdx.database import Database

from hapi_schema.db_currency import view_params_currency


def test_currency_view(run_view_test):
    """Check that currency view shows some columns."""
    view_currency = Database.prepare_view(view_params_currency.__dict__)
    run_view_test(
        view=view_currency,
        whereclause=(
            view_currency.c.code == "FOO",
            view_currency.c.name == "Foolandia BarBar",
        ),
    )
