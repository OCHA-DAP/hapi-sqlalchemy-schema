from typing import List

import pytest
from hdx.database import Database
from sqlalchemy import (
    insert,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.db_conflict_event import DBConflictEvent
from hapi_schema.db_currency import DBCurrency
from hapi_schema.db_dataset import DBDataset
from hapi_schema.db_food_price import (
    DBFoodPrice,
)
from hapi_schema.db_food_security import (
    DBFoodSecurity,
)
from hapi_schema.db_funding import DBFunding
from hapi_schema.db_humanitarian_needs import (
    DBHumanitarianNeeds,
)
from hapi_schema.db_location import DBLocation
from hapi_schema.db_national_risk import (
    DBNationalRisk,
)
from hapi_schema.db_operational_presence import (
    DBOperationalPresence,
)
from hapi_schema.db_org import DBOrg
from hapi_schema.db_org_type import DBOrgType
from hapi_schema.db_patch import DBPatch
from hapi_schema.db_population import DBPopulation
from hapi_schema.db_poverty_rate import DBPovertyRate
from hapi_schema.db_refugees import DBRefugees
from hapi_schema.db_resource import DBResource
from hapi_schema.db_sector import DBSector
from hapi_schema.db_wfp_commodity import DBWFPCommodity
from hapi_schema.db_wfp_market import DBWFPMarket
from hapi_schema.utils.base import Base
from hapi_schema.views import prepare_hapi_views
from sample_data.data_admin1 import data_admin1
from sample_data.data_admin2 import data_admin2
from sample_data.data_conflict_event import data_conflict_event
from sample_data.data_currency import data_currency
from sample_data.data_dataset import data_dataset
from sample_data.data_food_price import data_food_price
from sample_data.data_food_security import data_food_security
from sample_data.data_funding import data_funding
from sample_data.data_humanitarian_needs import data_humanitarian_needs
from sample_data.data_location import data_location
from sample_data.data_national_risk import data_national_risk
from sample_data.data_operational_presence import data_operational_presence
from sample_data.data_org import data_org
from sample_data.data_org_type import data_org_type
from sample_data.data_patch import data_patch
from sample_data.data_population import data_population
from sample_data.data_poverty_rate import data_poverty_rate
from sample_data.data_refugees import data_refugees
from sample_data.data_resource import data_resource
from sample_data.data_sector import data_sector
from sample_data.data_wfp_commodity import data_wfp_commodity
from sample_data.data_wfp_market import data_wfp_market


@pytest.fixture(scope="session")
def session():
    # Build the DB
    db_uri = "postgresql+psycopg://postgres:postgres@localhost:5432/hapitest"
    database = Database(
        db_uri=db_uri, recreate_schema=True, prepare_fn=prepare_hapi_views
    )
    session = database.get_session()

    # Populate all tables
    session.execute(insert(DBDataset), data_dataset)
    session.execute(insert(DBResource), data_resource)

    session.execute(insert(DBLocation), data_location)
    session.execute(insert(DBAdmin1), data_admin1)
    session.execute(insert(DBAdmin2), data_admin2)

    session.execute(insert(DBOrgType), data_org_type)
    session.execute(insert(DBOrg), data_org)
    session.execute(insert(DBSector), data_sector)
    session.execute(insert(DBWFPCommodity), data_wfp_commodity)
    session.execute(insert(DBWFPMarket), data_wfp_market)
    session.execute(insert(DBCurrency), data_currency)

    session.execute(insert(DBConflictEvent), data_conflict_event)
    session.execute(insert(DBFunding), data_funding)
    session.execute(insert(DBNationalRisk), data_national_risk)
    session.execute(insert(DBPopulation), data_population)
    session.execute(insert(DBOperationalPresence), data_operational_presence)
    session.execute(insert(DBPovertyRate), data_poverty_rate)
    session.execute(insert(DBRefugees), data_refugees)
    session.execute(insert(DBFoodSecurity), data_food_security)
    session.execute(insert(DBFoodPrice), data_food_price)
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


@pytest.fixture(scope="session")
def run_indexes_test(session):
    def _run_indexes_test(target_table: str, expected_indexes: str):
        """Test that the expected indexes are in a specified table"""
        Base.metadata.create_all(session.get_bind())
        Base.metadata.reflect(bind=session.get_bind(), views=True)
        columns = Base.metadata.tables[target_table].columns

        found_indexes = []

        for column in columns:
            if column.index:
                found_indexes.append(column.name)

        assert set(expected_indexes) == set(found_indexes)

    return _run_indexes_test


@pytest.fixture(scope="session")
def run_primary_keys_test(session):
    def _run_primary_keys_test(target_table: str, expected_primary_keys: str):
        """Test that the expected primary_keys are in a specified table"""
        Base.metadata.create_all(session.get_bind())
        Base.metadata.reflect(bind=session.get_bind(), views=True)
        columns = Base.metadata.tables[target_table].columns

        found_primary_keys = []

        for column in columns:
            if column.primary_key:
                found_primary_keys.append(column.name)

        assert set(expected_primary_keys) == set(found_primary_keys)

    return _run_primary_keys_test


@pytest.fixture(scope="session")
def run_columns_test(session):
    def _run_columns_test(target_table: str, target_view: str, view_params):
        """Test that a table has the same columns as its corresponding view"""
        _ = Database.prepare_view(view_params.__dict__)
        Base.metadata.create_all(session.get_bind())
        Base.metadata.reflect(bind=session.get_bind(), views=True)
        table_columns = Base.metadata.tables[target_table].columns
        view_columns = Base.metadata.tables[target_view].columns

        table_column_names = [x.name for x in table_columns]
        view_column_names = [x.name for x in view_columns]

        assert set(table_column_names) == set(view_column_names)

    return _run_columns_test
