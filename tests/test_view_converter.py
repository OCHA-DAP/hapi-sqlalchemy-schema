from hdx.database.views import build_view
from sqlalchemy import Table

from hapi_schema.db_admin1 import view_params_admin1
from hapi_schema.utils.base import Base

columns = None


def test_admin1_view_table(engine):
    """Check that admin1 view references location."""
    global columns
    _ = build_view(view_params_admin1.__dict__)
    Base.metadata.create_all(engine)
    # whereclause = (
    #     view_admin1.c.id == 1,
    #     view_admin1.c.location_code == "FOO",
    # )
    # select_instance = view_admin1.select().where(*whereclause)
    # select_instance.compile(bind=engine)
    # result = engine.connect().execute(select_instance)

    # result = result.fetchone()

    # print(result, flush=True)

    # view_metadata = MetaData().reflect(views=True)

    Base.metadata.reflect(bind=engine, views=True)

    columns = Base.metadata.tables["admin1_view"].columns
    # for item in dir(columns[0]):
    #     if not item.startswith("_"):
    #         print(item, getattr(columns[0], item), flush=True)
    # print(dir(Base.metadata), flush=True)
    new_columns = []
    for column in columns:
        new_column = column.copy()
        if column.name == "id":
            column.primary_key = True
        print(
            column.name,
            column.primary_key,
            column.type,
            column.unique,
            column.nullable,
            column.index,
            flush=True,
        )
        new_columns.append(new_column)
    # view_metadata.
    # view_metadata = Base.metadata.tables[
    #     "admin1"
    # ]  # .keys()  # ["admin1_view"]
    # print(view_metadata, flush=True)

    # Create the Metadata Object
    # metadata_obj = MetaData()

    # Define the profile table

    # database name
    admin1_vat = Table("admin1_vat", Base.metadata, *new_columns)

    print(admin1_vat)
    Base.metadata.create_all(engine)

    print(Base.metadata.tables.keys(), flush=True)

    # class DBAdmin1vat(Base):
    #     __tablename__ = "admin1_vat"

    #     columns = columns

    assert False
