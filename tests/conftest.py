import pytest
from sqlalchemy import create_engine, insert, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_age_range import DBAgeRange
from hapi_schema.db_dataset import DBDataset
from hapi_schema.db_food_security import DBFoodSecurity
from hapi_schema.db_gender import DBGender
from hapi_schema.db_humanitarian_needs import DBHumanitarianNeeds
from hapi_schema.db_ipc_phase import DBIpcPhase
from hapi_schema.db_ipc_type import DBIpcType
from hapi_schema.db_location import DBLocation
from hapi_schema.db_national_risk import DBNationalRisk
from hapi_schema.db_operational_presence import (
    DBOperationalPresence,
)
from hapi_schema.db_org import DBOrg
from hapi_schema.db_org_type import DBOrgType
from hapi_schema.db_population import DBPopulation
from hapi_schema.db_population_group import DBPopulationGroup
from hapi_schema.db_population_status import DBPopulationStatus
from hapi_schema.db_resource import DBResource
from hapi_schema.db_sector import DBSector
from hapi_schema.utils.base import Base
from sample_data.data_admin1 import data_admin1
from sample_data.data_admin2 import data_admin2
from sample_data.data_age_range import data_age_range
from sample_data.data_dataset import data_dataset
from sample_data.data_food_security import data_food_security
from sample_data.data_gender import data_gender
from sample_data.data_humanitarian_needs import data_humanitarian_needs
from sample_data.data_ipc_phase import data_ipc_phase
from sample_data.data_ipc_type import data_ipc_type
from sample_data.data_location import data_location
from sample_data.data_national_risk import data_national_risk
from sample_data.data_operational_presence import data_operational_presence
from sample_data.data_org import data_org
from sample_data.data_org_type import data_org_type
from sample_data.data_population import data_population
from sample_data.data_population_group import data_population_group
from sample_data.data_population_status import data_population_status
from sample_data.data_resource import data_resource
from sample_data.data_sector import data_sector


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(url="sqlite:///:memory:")

    # Execute pragma statement to enable foreign key constraints
    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys = ON;"))

    # Build the DB
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    # Populate all tables
    session.execute(insert(DBDataset), data_dataset)
    session.execute(insert(DBResource), data_resource)

    session.execute(insert(DBLocation), data_location)
    session.execute(insert(DBAdmin1), data_admin1)
    session.execute(insert(DBAdmin2), data_admin2)

    session.execute(insert(DBPopulationStatus), data_population_status)
    session.execute(insert(DBPopulationGroup), data_population_group)
    session.execute(insert(DBOrgType), data_org_type)
    session.execute(insert(DBOrg), data_org)
    session.execute(insert(DBSector), data_sector)
    session.execute(insert(DBIpcPhase), data_ipc_phase)
    session.execute(insert(DBIpcType), data_ipc_type)
    session.execute(insert(DBGender), data_gender)
    session.execute(insert(DBAgeRange), data_age_range)

    session.execute(insert(DBNationalRisk), data_national_risk)
    session.execute(insert(DBPopulation), data_population)
    session.execute(insert(DBOperationalPresence), data_operational_presence)
    session.execute(insert(DBFoodSecurity), data_food_security)
    session.execute(insert(DBHumanitarianNeeds), data_humanitarian_needs)

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


@pytest.fixture(scope="session")
def run_constraints_test(engine):
    def _run_constraints_test(new_row, expected_constraint):
        Base.metadata.create_all(engine)
        session = sessionmaker(bind=engine)()
        session.add(new_row)
        with pytest.raises(IntegrityError) as exc_info:
            session.commit()
        assert expected_constraint in str(exc_info.value)

    return _run_constraints_test
