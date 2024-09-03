import inspect
import os
from importlib import import_module

from sqlalchemy.sql.expression import union_all

from hapi_schema.utils.base import Base
from hapi_schema.utils.view_params import ViewParams

try:
    from hdx.database import Database
except ImportError:
    Database = None
    pass


def prepare_hapi_views():
    # Programmatically get views and prepare them for creation.
    # Views must be in files with filename of form: db_{name}.py in the same
    # directory. Views must be named like this: view_params_{name}.
    global view_availability
    path = inspect.getabsfile(prepare_hapi_views)
    dirpath, _ = os.path.split(path)
    availability_stmts = []
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
                Database.prepare_view(view_params.__dict__)
                availability_stmt = getattr(
                    module, f"availability_stmt_{table}"
                )
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

    # Return this view (to simplify unit tests)
    return Database.prepare_view(view_params_availability.__dict__)
