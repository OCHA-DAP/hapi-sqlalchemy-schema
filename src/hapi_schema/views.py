import inspect
import os
from importlib import import_module

try:
    from hdx.database import Database
except ImportError:
    Database = None
    pass


def prepare_hapi_views():
    # Programmatically get views and prepare them for creation.
    # Views must be in files with filename of form: db_{name}.py in the same
    # directory. Views must be named like this: view_params_{name}.
    path = inspect.getabsfile(prepare_hapi_views)
    dirpath, _ = os.path.split(path)
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
            except AttributeError:
                pass
