import inspect
import os
from importlib import import_module
from typing import Any, Dict, Tuple

from sqlalchemy import ColumnElement, Label, TableClause, and_, case, or_
from sqlalchemy.sql.expression import union_all

from hapi_schema.db_admin1 import DBAdmin1
from hapi_schema.db_admin2 import DBAdmin2
from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams

try:
    from hdx.database import Database
except ImportError:
    Database = None
    pass


def prepare_hapi_views() -> Dict[str, TableClause]:
    # Programmatically get views and prepare them for creation.
    # Views must be in files with filename of form: db_{name}.py in the same
    # directory. Views must be named like this: view_params_{name}.
    global view_availability
    path = inspect.getabsfile(prepare_hapi_views)
    dirpath, _ = os.path.split(path)
    availability_stmts = []
    views = {}
    for path in os.listdir(dirpath):
        if os.path.isdir(path):
            continue
        _, filepath = os.path.split(path)
        if filepath.startswith("db_") and filepath.endswith(".py"):
            filename = filepath[:-3]
            module = import_module(f"hapi_schema.{filename}")
            table = filename[3:]
            try:
                view_params = getattr(module, f"view_params_{table}")
                views[table] = Database.prepare_view(view_params.__dict__)
                availability_stmt = getattr(module, f"availability_stmt_{table}")
                if availability_stmt is not None:
                    availability_stmts.append(availability_stmt)
            except AttributeError:
                pass

    # Also prepare a data-availability view, which is a union of availability for each subcategory
    view_params_availability = ViewParams(
        name="data_availability_view",
        metadata=Base.metadata,
        selectable=union_all(*availability_stmts),
    )

    views["data_availability"] = Database.prepare_view(
        view_params_availability.__dict__
    )
    return views


def get_admin1_when(table: Any) -> Tuple[ColumnElement, int]:
    return (
        or_(
            and_(
                table.provider_admin1_name.is_not(None),
                table.provider_admin1_name != "",
            ),
            DBAdmin1.is_unspecified.is_(False),
        ),
        1,
    )


def get_admin1_case(table: Any) -> Label:
    return case(
        get_admin1_when(table),
        else_=0,
    ).label("admin_level")


def get_admin2_case(table: Any) -> Label:
    return case(
        (
            or_(
                and_(
                    table.provider_admin2_name.is_not(None),
                    table.provider_admin2_name != "",
                ),
                DBAdmin2.is_unspecified.is_(False),
            ),
            2,
        ),
        get_admin1_when(table),
        else_=0,
    ).label("admin_level")
