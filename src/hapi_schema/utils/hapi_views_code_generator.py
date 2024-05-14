#!/usr/bin/env python
# encoding: utf-8
"""
This script is designed to print a sqlalchemy table class from a view.

The code is configured using the `view_as_table_definitions.toml` file and then with an invocation like:

`./view_as_table_code_generator.py patch_view`

This will pick up the appropriate section from the toml file

Ian Hopkinson 2024-05-09
"""

import os
import sys
from importlib import import_module

import tomllib
from hdx.database import Database

# Edit this to import the view parameters
from hapi_schema.utils.base import Base
from hapi_schema.views import prepare_hapi_views


def parse_toml():
    target_view = "national_risk_view"
    if len(sys.argv) == 2:
        target_view = sys.argv[1]

    config_file_path = os.path.join(
        os.path.dirname(__file__), "view_as_table_definitions.toml"
    )
    with open(config_file_path, "rb") as file_handle:
        config = tomllib.load(file_handle)

    parameters = None
    for table in config["tables"]:
        if table["target_view"] == target_view:
            parameters = table
            break

    table_code = create_table_code(parameters)
    for line in table_code:
        print(line, flush=True)


def create_table_code(parameters: dict) -> list[str]:
    # Change these the target_view, prepare_view, expected_primary_keys and expected_indexes
    target_view = parameters["target_view"]
    expected_primary_keys = parameters["expected_primary_keys"]
    expected_indexes = parameters["expected_indexes"]
    expected_nullables = parameters["expected_nullables"]

    view_params_dict = dynamically_load_view_params(
        parameters["db_module"], parameters["view_params_name"]
    )
    _ = Database.prepare_view(view_params_dict)
    #
    session = make_session()
    target_table = target_view.replace("view", "vat")
    Base.metadata.create_all(session.get_bind())
    Base.metadata.reflect(bind=session.get_bind(), views=True)
    columns = Base.metadata.tables[target_view].columns

    # Make Preamble
    table_code = []
    table_code.append(
        f"\nfrom hapi_schema.{parameters['db_module']} import {parameters['view_params_name']}\n"
    )

    table_code.append(
        f"{parameters['target_view']} = view({parameters['view_params_name']}.name, Base.metadata, {parameters['view_params_name']}.selectable)\n"
    )

    new_columns, table_body_code = make_table_template_from_view(
        target_table,
        columns,
        expected_indexes=expected_indexes,
        expected_nullables=expected_nullables,
        expected_primary_keys=expected_primary_keys,
    )

    table_code.extend(table_body_code)

    return table_code


def make_table_template_from_view(
    target_table,
    columns,
    expected_indexes=None,
    expected_primary_keys=None,
    expected_nullables=None,
):
    if expected_primary_keys is None:
        expected_primary_keys = ["id"]
    if expected_indexes is None:
        expected_indexes = []
    if expected_nullables is None:
        expected_nullables = []

    table_code = []
    # Make a CamelCase name from the supplied table name
    # admin1_vat-> Admin1View
    class_name = (
        target_table.replace("_vat", "")
        .replace("_", " ")
        .title()
        .replace(" ", "")
        + "View"
    )

    source_view = target_table.replace("_vat", "_view")
    table_code.append(f"class {class_name}(Base):")
    table_code.append(f"    __table__ = {source_view}")

    new_columns = []
    for column in columns:
        new_column = column._copy()
        column_type = str(column.type)
        mapped_type_1 = column_type
        if column_type == "INTEGER":
            mapped_type_1 = "int"
        elif column_type.startswith("VARCHAR"):
            mapped_type_1 = "str"
        elif column_type == "BOOLEAN":
            mapped_type_1 = "bool"
        elif column_type in ["DATETIME", "TIMESTAMP"]:
            mapped_type_1 = "DateTime"
        elif column_type in ["FLOAT", "DOUBLE PRECISION"]:
            mapped_type_1 = "float"
        elif column_type == "TEXT":
            mapped_type_1 = "str"
        table_code.append(
            f"    {column.name}: Mapped[{mapped_type_1}] = column_property({source_view}.c.{column.name})"
        )

        new_columns.append(new_column)
    return new_columns, table_code


def make_session():
    db_uri = "postgresql+psycopg://postgres:postgres@localhost:5432/hapitest"
    database = Database(
        db_uri=db_uri, recreate_schema=True, prepare_fn=prepare_hapi_views
    )
    session = database.get_session()
    return session


def dynamically_load_view_params(db_module, view_name):
    module = import_module(f"hapi_schema.{db_module}")
    target_view_params = getattr(module, f"{view_name}")

    return target_view_params.__dict__


if __name__ == "__main__":
    parse_toml()
    # output_table_code_to_stdout()
