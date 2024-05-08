import pytest
from hdx.database import Database
from sqlalchemy import Table

# Edit this to import the view parameters
from hapi_schema.db_national_risk import (
    view_params_national_risk,
)
from hapi_schema.utils.base import Base


@pytest.mark.skip(reason="This is not a real test")
def test_output_table_code_to_stdout(session):
    # Change these two
    target_view = "national_risk_view"
    _ = Database.prepare_view(view_params_national_risk.__dict__)
    expected_primary_keys = [
        "location_ref",
        "reference_period_start",
        "reference_period_end",
    ]

    expected_indexes = []
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

    print(Base.metadata.tables.keys(), flush=True)

    assert target_table in Base.metadata.tables.keys()
    assert False


def make_table_template_from_view(
    target_table, columns, expected_indexes, primary_keys=["id"]
):
    print(f"class DB{target_table}(Base):", flush=True)
    print(f"\t__tablename__ = '{target_table}'", flush=True)
    new_columns = []
    for column in columns:
        new_column = column.copy()
        if column.name == "id":
            column.primary_key = True

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
            f"\t{column.name}: Mapped[{mapped_type_1}] = mapped_column({mapped_type_2}{primary_key_str}{index_str})"
        )

        new_columns.append(new_column)
    return new_columns
