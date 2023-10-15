import pytest
from hdx.database.views import view
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker

from hapi_schema.db_admin1 import DBAdmin1, admin1_view_params
from hapi_schema.db_admin2 import DBAdmin2, admin2_view_params
from hapi_schema.db_age_range import DBAgeRange, age_range_view_params
from hapi_schema.db_dataset import DBDataset, dataset_view_params
from hapi_schema.db_gender import DBGender, gender_view_params
from hapi_schema.db_location import DBLocation, location_view_params
from hapi_schema.db_operational_presence import (
    DBOperationalPresence,
    operational_presence_view_params,
)
from hapi_schema.db_org import DBOrg, org_view_params
from hapi_schema.db_org_type import DBOrgType, org_type_view_params
from hapi_schema.db_population import DBPopulation, population_view_params
from hapi_schema.db_resource import DBResource, resource_view_params
from hapi_schema.db_sector import DBSector, sector_view_params
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


@pytest.fixture
def session():
    engine = create_engine(url="sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_tables_and_views(session):
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

    # Create all views
    view(**admin1_view_params.__dict__)
    view(**admin2_view_params.__dict__)
    view(**admin2_view_params.__dict__)
    view(**age_range_view_params.__dict__)
    view(**dataset_view_params.__dict__)
    view(**gender_view_params.__dict__)
    view(**location_view_params.__dict__)
    view(**operational_presence_view_params.__dict__)
    view(**org_view_params.__dict__)
    view(**org_type_view_params.__dict__)
    view(**population_view_params.__dict__)
    view(**resource_view_params.__dict__)
    view(**sector_view_params.__dict__)
