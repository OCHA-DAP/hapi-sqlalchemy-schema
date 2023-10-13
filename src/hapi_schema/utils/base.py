try:
    from hdx.database.no_timezone import Base

except ImportError:
    from sqlalchemy.orm import DeclarativeBase

    class Base(DeclarativeBase):
        pass
