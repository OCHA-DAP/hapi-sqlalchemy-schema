import string

from sqlalchemy import create_engine

from hapi_schema.utils.base import Base


def test_db_patches(capfd):
    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine)

    sql_table_creation_code = """CREATE TABLE patches (
        id INTEGER NOT NULL,
        patch_sequence_number INTEGER NOT NULL,
        commit_hash VARCHAR(48) NOT NULL,
        commit_date DATETIME NOT NULL,
        patch_path VARCHAR(128) NOT NULL,
        permanent_download_url VARCHAR(1024) NOT NULL,
        state VARCHAR(10) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (commit_hash),
        UNIQUE (permanent_download_url)
)
"""
    captured_sql, _ = capfd.readouterr()
    assert sql_table_creation_code.translate(
        str.maketrans("", "", string.whitespace)
    ) in captured_sql.translate(str.maketrans("", "", string.whitespace))
