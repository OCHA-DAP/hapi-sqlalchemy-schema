import pytest
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_age_range import DBAgeRange
from hapi_schema.db_dataset import DBDataset
from hapi_schema.db_gender import DBGender
from hapi_schema.db_location import DBLocation
from hapi_schema.db_operational_presence import (
    DBOperationalPresence,
)
from hapi_schema.db_org import DBOrg
from hapi_schema.db_org_type import DBOrgType
from hapi_schema.db_population import DBPopulation
from hapi_schema.db_resource import DBResource
from hapi_schema.db_sector import DBSector
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


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(url="sqlite:///:memory:")

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

    return engine


@pytest.fixture(scope="session")
def run_view_test(engine):
    def _run_view_test(view, whereclause):
        Base.metadata.create_all(engine)
        select_instance = view.select().where(*whereclause)
        select_instance.compile(bind=engine)
        result = engine.connect().execute(select_instance)
        assert result.fetchone()

    return _run_view_test
