#!/usr/bin/env python
# encoding: utf-8
"""
This script is designed to print a sqlalchemy table class from a view.
To use it the code needs to be edited appropriately before running it:

1. Update the import of the view_params below to pick the right view
2. Change the target_view string to provide the new table name - conventionally this ends "_vat"
3. Fill in the expected_primary_keys and expected_indexes lists
4. Run the script - the class definition is output to console
5. Copy the class definition to the file from which the view_params were
6. Create a test of the view following the style, of test_operational_presence.py/test_operational_presence_vat -
   this requires the expected_primary_keys and expected_indexes created in step 3 and will check the "view_as_tables"
   columns match the view columns as well as checking the primary_keys and indexes.

Ian Hopkinson 2024-05-09
"""

from hdx.database import Database
from sqlalchemy import Table

# Edit this to import the view parameters
from hapi_schema.db_national_risk import (
    view_params_national_risk,
)
from hapi_schema.utils.base import Base
from hapi_schema.views import prepare_hapi_views


def output_table_code_to_stdout():
    # Change these the target_view, prepare_view, expected_primary_keys and expected_indexes
    target_view = "national_risk_view"
    _ = Database.prepare_view(view_params_national_risk.__dict__)
    expected_primary_keys = [
        "location_ref",
        "reference_period_start",
        "reference_period_end",
    ]

    expected_indexes = []
    #
    session = make_session()
    target_table = target_view.replace("view", "vat")
    Base.metadata.create_all(session.get_bind())
    Base.metadata.reflect(bind=session.get_bind(), views=True)
    columns = Base.metadata.tables[target_view].columns

    new_columns = make_table_template_from_view(
        target_table,
        columns,
        expected_indexes,
        primary_keys=expected_primary_keys,
    )

    _ = Table(target_table, Base.metadata, *new_columns)

    Base.metadata.create_all(session.get_bind())

    assert target_table in Base.metadata.tables.keys()


def make_table_template_from_view(
    target_table, columns, expected_indexes, primary_keys=["id"]
):
    # Make a CamelCase name from the supplied table name
    class_name = (
        "DB"
        + target_table.replace("_vat", "")
        .replace("_", " ")
        .title()
        .replace(" ", "")
        + "_vat"
    )
    print(f"class {class_name}(Base):", flush=True)
    print(f"    __tablename__ = '{target_table}'", flush=True)

    new_columns = []
    for column in columns:
        new_column = column._copy()
        primary_key_str = ""
        index_str = ""
        if column.name in primary_keys:
            primary_key_str = ", primary_key=True"
        if column.name in expected_indexes:
            index_str = ", index=True"
        column_type = str(column.type)
        mapped_type_1 = column_type
        mapped_type_2 = column_type
        if column_type == "INTEGER":
            mapped_type_1 = "int"
            mapped_type_2 = "Integer"
        elif column_type.startswith("VARCHAR"):
            mapped_type_1 = "str"
            mapped_type_2 = column_type.replace("VARCHAR", "String")
        elif column_type == "BOOLEAN":
            mapped_type_1 = "bool"
            mapped_type_2 = "Boolean"
        elif column_type in ["DATETIME", "TIMESTAMP"]:
            mapped_type_1 = "datetime"
            mapped_type_2 = "DateTime"
        elif column_type in ["FLOAT", "DOUBLE PRECISION"]:
            mapped_type_1 = "float"
            mapped_type_2 = "Float"
        elif column_type == "TEXT":
            mapped_type_1 = "str"
            mapped_type_2 = "Text"
        print(
            f"    {column.name}: Mapped[{mapped_type_1}] = mapped_column({mapped_type_2}{primary_key_str}{index_str})"
        )

        new_columns.append(new_column)
    return new_columns


def make_session():
    db_uri = "postgresql+psycopg://postgres:postgres@localhost:5432/hapitest"
    database = Database(
        db_uri=db_uri, recreate_schema=True, prepare_fn=prepare_hapi_views
    )
    session = database.get_session()
    return session


if __name__ == "__main__":
    output_table_code_to_stdout()
