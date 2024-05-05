from hdx.database.views import build_view
from sqlalchemy import Table

# Edit this to import the view parameters
from hapi_schema.db_admin1 import view_params_admin1
from hapi_schema.utils.base import Base


def test_output_table_code_to_stdout(engine):
    # Change these two
    target_view = "admin1_view"
    _ = build_view(view_params_admin1.__dict__)

    target_table = target_view.replace("view", "vat")
    expected_indexes = [
        "reference_period_start",
        "reference_period_end",
        "hapi_updated_date",
        "hapi_replaced_date",
    ]

    Base.metadata.create_all(engine)
    Base.metadata.reflect(bind=engine, views=True)
    columns = Base.metadata.tables[target_view].columns

    new_columns = make_table_template_from_view(
        target_table, columns, expected_indexes
    )

    _ = Table(target_table, Base.metadata, *new_columns)

    Base.metadata.create_all(engine)

    print(Base.metadata.tables.keys(), flush=True)

    assert target_table in Base.metadata.tables.keys()
    assert False


def make_table_template_from_view(target_table, columns, expected_indexes):
    print(f"class DB{target_table}(Base):", flush=True)
    print(f"\t__tablename__ = '{target_table}'", flush=True)
    new_columns = []
    for column in columns:
        new_column = column.copy()
        if column.name == "id":
            column.primary_key = True

        primary_key_str = ""
        index_str = ""
        if column.name == "id":
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
        print(
            f"\t{column.name}: Mapped[{mapped_type_1}] = mapped_column({mapped_type_2}{primary_key_str}{index_str})"
        )

        new_columns.append(new_column)
    return new_columns
