import string

from sqlalchemy import create_engine

from hapi_schema.utils.base import Base


def test_db_patch(capfd):
    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine, tables=[Base.metadata.tables["patch"]])

    sql_table_creation_code = """CREATE TABLE patch (
        id INTEGER NOT NULL,
        patch_sequence_number INTEGER NOT NULL,
        commit_hash VARCHAR(48) NOT NULL,
        commit_date DATETIME NOT NULL,
        patch_path VARCHAR(512) NOT NULL,
        patch_permalink_url VARCHAR(1024) NOT NULL,
        patch_target VARCHAR(128) NOT NULL,
        patch_hash VARCHAR(48) NOT NULL,
        state VARCHAR(10) NOT NULL,
        execution_date DATETIME,
        PRIMARY KEY (id)
)
"""
    sql_patch_sequence_number_index_creation = """
    CREATE INDEX ix_patch_patch_sequence_number ON patch (patch_sequence_number)
    """
    sql_state_index_creation = (
        """CREATE INDEX ix_patch_state ON patch (state)"""
    )

    captured_sql, _ = capfd.readouterr()

    for sql_statements in [
        sql_table_creation_code,
        sql_patch_sequence_number_index_creation,
        sql_state_index_creation,
    ]:
        assert sql_statements.translate(
            str.maketrans("", "", string.whitespace)
        ) in captured_sql.translate(str.maketrans("", "", string.whitespace))
