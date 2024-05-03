from typing import List

import pytest
from hdx.database.views import build_views
from sqlalchemy import (
    create_engine,
    insert,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.ddl import (
    CreateSchema,
    DropSchema,
)

from hapi_schema.db_admin1 import DBAdmin1, view_params_admin1
from hapi_schema.db_admin2 import DBAdmin2, view_params_admin2
from hapi_schema.db_dataset import DBDataset, view_params_dataset
from hapi_schema.db_food_security import (
    DBFoodSecurity,
    view_params_food_security,
)
from hapi_schema.db_humanitarian_needs import (
    DBHumanitarianNeeds,
    view_params_humanitarian_needs,
)
from hapi_schema.db_ipc_phase import DBIpcPhase, view_params_ipc_phase
from hapi_schema.db_ipc_type import DBIpcType, view_params_ipc_type
from hapi_schema.db_location import DBLocation, view_params_location
from hapi_schema.db_national_risk import (
    DBNationalRisk,
    view_params_national_risk,
)
from hapi_schema.db_operational_presence import (
    DBOperationalPresence,
    view_params_operational_presence,
)
from hapi_schema.db_org import DBOrg, view_params_org
from hapi_schema.db_org_type import DBOrgType, view_params_org_type
from hapi_schema.db_patch import DBPatch
from hapi_schema.db_population import DBPopulation, view_params_population
from hapi_schema.db_resource import DBResource, view_params_resource
from hapi_schema.db_sector import DBSector, view_params_sector
from hapi_schema.utils.base import Base
from sample_data.data_admin1 import data_admin1
from sample_data.data_admin2 import data_admin2
from sample_data.data_dataset import data_dataset
from sample_data.data_food_security import data_food_security
from sample_data.data_humanitarian_needs import data_humanitarian_needs
from sample_data.data_ipc_phase import data_ipc_phase
from sample_data.data_ipc_type import data_ipc_type
from sample_data.data_location import data_location
from sample_data.data_national_risk import data_national_risk
from sample_data.data_operational_presence import data_operational_presence
from sample_data.data_org import data_org
from sample_data.data_org_type import data_org_type
from sample_data.data_patch import data_patch
from sample_data.data_population import data_population
from sample_data.data_resource import data_resource
from sample_data.data_sector import data_sector


@pytest.fixture(scope="session")
def session():
    engine = create_engine(
        url="postgresql+psycopg://postgres:postgres@localhost:5432/hapitest"
    )

    # Create an empty schema
    with engine.connect() as connection:
        connection.execute(DropSchema("public", cascade=True, if_exists=True))
        connection.commit()
        connection.execute(CreateSchema("public", if_not_exists=True))
        connection.commit()

    # Build the Views
    build_views(
        view_params_list=[
            view_params.__dict__
            for view_params in [
                view_params_admin1,
                view_params_admin2,
                view_params_dataset,
                view_params_food_security,
                view_params_humanitarian_needs,
                view_params_ipc_phase,
                view_params_ipc_type,
                view_params_location,
                view_params_national_risk,
                view_params_operational_presence,
                view_params_org,
                view_params_org_type,
                view_params_population,
                view_params_resource,
                view_params_sector,
            ]
        ]
    )

    # Build the DB
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()

    # Populate all tables
    session.execute(insert(DBDataset), data_dataset)
    session.execute(insert(DBResource), data_resource)

    session.execute(insert(DBLocation), data_location)
    session.execute(insert(DBAdmin1), data_admin1)
    session.execute(insert(DBAdmin2), data_admin2)

    session.execute(insert(DBOrgType), data_org_type)
    session.execute(insert(DBOrg), data_org)
    session.execute(insert(DBSector), data_sector)
    session.execute(insert(DBIpcPhase), data_ipc_phase)
    session.execute(insert(DBIpcType), data_ipc_type)

    session.execute(insert(DBNationalRisk), data_national_risk)
    session.execute(insert(DBPopulation), data_population)
    session.execute(insert(DBOperationalPresence), data_operational_presence)
    session.execute(insert(DBFoodSecurity), data_food_security)
    session.execute(insert(DBHumanitarianNeeds), data_humanitarian_needs)

    session.execute(insert(DBPatch), data_patch)

    session.commit()
    return session


@pytest.fixture(scope="session")
def run_view_test(session):
    def _run_view_test(view, whereclause):
        select_instance = view.select().where(*whereclause)
        result = session.execute(select_instance)
        assert result.fetchone()

    return _run_view_test


@pytest.fixture(scope="session")
def run_constraints_test(session):
    def _run_constraints_test(
        new_rows: List[DeclarativeMeta], expected_constraint: str
    ):
        """Test that a constraint will be triggered by passing its name
        and a list of one or more rows that violate it."""
        for new_row in new_rows:
            session.add(new_row)
        with pytest.raises(IntegrityError) as exc_info:
            session.commit()
        session.rollback()
        assert expected_constraint in str(exc_info.value)

    return _run_constraints_test
