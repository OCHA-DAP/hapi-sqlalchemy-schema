from hdx.database.views import build_view

from hapi_schema.db_population import view_params_population


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
            view_population.c.admin2_code == "FOO-001-XXX",
            view_population.c.admin1_code == "FOO-001",
            view_population.c.location_code == "FOO",
            view_population.c.gender_code == "f",
        ),
    )
