import hapi_schema.utils.sqlite  # noqa: F401 Registers SQLite-only DDL

try:
    from hdx.database.no_timezone import Base

except ImportError:
    from sqlalchemy.orm import DeclarativeBase

    class Base(DeclarativeBase):
        pass
