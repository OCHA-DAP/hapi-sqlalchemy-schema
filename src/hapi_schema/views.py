import inspect
import os
from importlib import import_module

from hdx.database.views import build_view


def build_hapi_views():
    # Programmatically get views and build them
    path = inspect.getabsfile(build_hapi_views)
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
                build_view(view_params.__dict__)
            except AttributeError:
                pass
