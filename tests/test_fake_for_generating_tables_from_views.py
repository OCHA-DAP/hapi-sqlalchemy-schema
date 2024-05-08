import pytest
from hdx.database import Database
from sqlalchemy import Table

# Edit this to import the view parameters
from hapi_schema.db_org import (
    view_params_org,
)
from hapi_schema.utils.base import Base


@pytest.mark.skip(reason="This is not a real test")
def test_output_table_code_to_stdout(engine):
    # Change these two
    target_view = "org_view"
    _ = Database.prepare_view(view_params_org.__dict__)
    primary_key = "id"

    expected_indexes = [
        "acronym",
        "dataset_hdx_provider_stub",
        "dataset_hdx_provider_name",
        "resource_update_date",
        "hapi_updated_date",
        "hapi_replaced_date",
        "reference_period_start",
        "reference_period_end",
    ]
    target_table = target_view.replace("view", "vat")
    Base.metadata.create_all(engine)
    Base.metadata.reflect(bind=engine, views=True)
    columns = Base.metadata.tables[target_view].columns

    new_columns = make_table_template_from_view(
        target_table, columns, expected_indexes, primary_key=primary_key
    )

    _ = Table(target_table, Base.metadata, *new_columns)

    Base.metadata.create_all(engine)

    print(Base.metadata.tables.keys(), flush=True)

    assert target_table in Base.metadata.tables.keys()
    assert False


def make_table_template_from_view(
    target_table, columns, expected_indexes, primary_key="id"
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
        if column.name == primary_key:
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
        elif column_type == "DATETIME":
            mapped_type_1 = "datetime"
            mapped_type_2 = "DateTime"
        elif column_type == "FLOAT":
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
