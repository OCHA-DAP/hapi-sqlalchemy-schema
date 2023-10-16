from hdx.database.views import build_view
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from hapi_schema.db_admin1 import DBAdmin1, view_params_admin1
from hapi_schema.db_admin2 import DBAdmin2, view_params_admin2
from hapi_schema.db_age_range import DBAgeRange, view_params_age_range
from hapi_schema.db_dataset import DBDataset, view_params_dataset
from hapi_schema.db_gender import DBGender, view_params_gender
from hapi_schema.db_location import DBLocation, view_params_location
from hapi_schema.db_operational_presence import (
    DBOperationalPresence,
    view_params_operational_presence,
)
from hapi_schema.db_org import DBOrg, view_params_org
from hapi_schema.db_org_type import DBOrgType, view_params_org_type
from hapi_schema.db_population import DBPopulation, view_params_population
from hapi_schema.db_resource import DBResource, view_params_resource
from hapi_schema.db_sector import DBSector, view_params_sector
from hapi_schema.utils.base import Base
from sample_data.data_admin1 import data_admin1
from sample_data.data_admin2 import data_admin2
from sample_data.data_age_range import data_age_range
from sample_data.data_dataset import data_dataset
from sample_data.data_gender import data_gender
from sample_data.data_location import data_location
from sample_data.data_operational_presence import data_operational_presence
from sample_data.data_org import data_org
from sample_data.data_org_type import data_org_type
from sample_data.data_population import data_population
from sample_data.data_resource import data_resource
from sample_data.data_sector import data_sector


def test_table_and_views():
    engine = create_engine(url="sqlite:///:memory:")

    # Create the views
    view_admin1 = build_view(view_params_admin1.__dict__)
    build_view(view_params_admin2.__dict__)
    build_view(view_params_age_range.__dict__)
    build_view(view_params_dataset.__dict__)
    build_view(view_params_gender.__dict__)
    build_view(view_params_location.__dict__)
    build_view(view_params_operational_presence.__dict__)
    build_view(view_params_org.__dict__)
    build_view(view_params_org_type.__dict__)
    build_view(view_params_population.__dict__)
    build_view(view_params_resource.__dict__)
    build_view(view_params_sector.__dict__)

    # Build the DB
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    # Populate all tables
    session.execute(insert(DBAdmin1), data_admin1)
    session.execute(insert(DBAdmin2), data_admin2)
    session.execute(insert(DBAgeRange), data_age_range)
    session.execute(insert(DBDataset), data_dataset)
    session.execute(insert(DBGender), data_gender)
    session.execute(insert(DBLocation), data_location)
    session.execute(insert(DBOperationalPresence), data_operational_presence)
    session.execute(insert(DBOrg), data_org)
    session.execute(insert(DBOrgType), data_org_type)
    session.execute(insert(DBPopulation), data_population)
    session.execute(insert(DBResource), data_resource)
    session.execute(insert(DBSector), data_sector)

    session.commit()

    # Test all views

    # Admin1
    select_admin1 = view_admin1.select().where(
        view_admin1.c.id == 1, view_admin1.c.location_code == "FOO"
    )
    select_admin1.compile(bind=engine)
    result = engine.connect().execute(select_admin1)
    row = result.fetchone()
    assert row
