import string

from sqlalchemy import create_engine

from hapi_schema.utils.base import Base


def test_db_patch(capfd):
    engine = create_engine("sqlite://", echo=True)
    Base.metadata.create_all(engine, tables=[Base.metadata.tables["patch"]])

    sql_table_creation_code = """CREATE TABLE patch (
        id INTEGER NOT NULL CHECK (id BETWEEN -2147483648 AND 2147483647),
        patch_sequence_number INTEGER NOT NULL
            CHECK (patch_sequence_number BETWEEN -2147483648 AND 2147483647),
        commit_hash TEXT NOT NULL CHECK (instr(commit_hash, char(0)) = 0)
            CHECK (length(commit_hash) <= 48),
        commit_date TEXT NOT NULL CHECK (commit_date IS NULL OR
            (datetime(commit_date) IS NOT NULL
            AND date(substr(commit_date, 1, 10)) IS substr(commit_date, 1, 10))),
        patch_path TEXT NOT NULL CHECK (instr(patch_path, char(0)) = 0)
            CHECK (length(patch_path) <= 512),
        patch_permalink_url TEXT NOT NULL
            CHECK (instr(patch_permalink_url, char(0)) = 0)
            CHECK (length(patch_permalink_url) <= 1024),
        patch_target TEXT NOT NULL CHECK (instr(patch_target, char(0)) = 0)
            CHECK (length(patch_target) <= 128),
        patch_hash TEXT NOT NULL CHECK (instr(patch_hash, char(0)) = 0)
            CHECK (length(patch_hash) <= 48),
        state TEXT NOT NULL
            CHECK (state IN ('discovered', 'executed', 'failed', 'canceled')),
        execution_date TEXT CHECK (execution_date IS NULL OR
            (datetime(execution_date) IS NOT NULL
            AND date(substr(execution_date, 1, 10))
                IS substr(execution_date, 1, 10))),
        PRIMARY KEY (id)
) STRICT
"""
    sql_patch_sequence_number_index_creation = """
    CREATE INDEX ix_patch_patch_sequence_number ON patch (patch_sequence_number)
    """
    sql_state_index_creation = """CREATE INDEX ix_patch_state ON patch (state)"""

    captured_sql, _ = capfd.readouterr()

    for sql_statements in [
        sql_table_creation_code,
        sql_patch_sequence_number_index_creation,
        sql_state_index_creation,
    ]:
        assert sql_statements.translate(
            str.maketrans("", "", string.whitespace)
        ) in captured_sql.translate(str.maketrans("", "", string.whitespace))
