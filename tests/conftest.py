import pytest
from hapi_schema.utils.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def session():
    db_uri = "sqlite:///:memory:"
    engine = create_engine(url=db_uri)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()
    return session
