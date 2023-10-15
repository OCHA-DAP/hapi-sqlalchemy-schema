from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_age_range import DBAgeRange
from hapi_schema.db_dataset import DBDataset
from hapi_schema.db_gender import DBGender
from hapi_schema.db_location import DBLocation
from hapi_schema.db_operational_presence import DBOperationalPresence
from hapi_schema.db_org import DBOrg
from hapi_schema.db_org_type import DBOrgType
from hapi_schema.db_population import DBPopulation
from hapi_schema.db_resource import DBResource
from hapi_schema.db_sector import DBSector
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
from sqlalchemy import insert


def test_all_dbs(session):
    # Metadata
    session.execute(insert(DBDataset), data_dataset)
    session.execute(insert(DBResource), data_resource)
    # Location
    session.execute(insert(DBLocation), data_location)
    session.execute(insert(DBAdmin1), data_admin1)
    session.execute(insert(DBAdmin2), data_admin2)
    # Demographics
    session.execute(insert(DBAgeRange), data_age_range)
    session.execute(insert(DBGender), data_gender)
    # Organizations
    session.execute(insert(DBSector), data_sector)
    session.execute(insert(DBOrgType), data_org_type)
    session.execute(insert(DBOrg), data_org)
    # Themes
    session.execute(insert(DBOperationalPresence), data_operational_presence)
    session.execute(insert(DBPopulation), data_population)
