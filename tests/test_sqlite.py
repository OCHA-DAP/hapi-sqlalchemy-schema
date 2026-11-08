"""SQLite rejects the values Postgres rejects (see hapi_schema.utils.sqlite).
The sqlite_session fixture loading all sample data checks valid values are
still accepted."""

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError


@pytest.mark.parametrize(
    "table, column, value",
    [
        ("population", "population", "lots"),  # STRICT INTEGER
        ("funding", "funding_usd", "lots"),  # STRICT REAL
        ("population", "population", 2**31),  # 32-bit range
        ("population", "gender", "xyz"),  # Enum
        ("population", "age_range", "x" * 33),  # String(32)
        ("population", "provider_admin1_name", "a\x00b"),  # NUL
        ("location", "has_hrp", 2),  # Boolean
        ("population", "reference_period_end", "not a date"),
        ("population", "reference_period_end", "2024-02-30 00:00:00.000000"),
        ("admin1", "location_ref", 99999),  # Foreign key
    ],
)
def test_sqlite_rejects(sqlite_session, table, column, value):
    with pytest.raises(IntegrityError):
        sqlite_session.execute(
            text(
                f"UPDATE {table} SET {column} = :value "
                f"WHERE rowid = (SELECT min(rowid) FROM {table})"
            ),
            {"value": value},
        )
    sqlite_session.rollback()


def test_sqlite_rejects_nan(sqlite_session):
    with pytest.raises(ValueError, match="NaN"):
        sqlite_session.execute(
            text("UPDATE wfp_market SET lat = :value"), {"value": float("nan")}
        )
    sqlite_session.rollback()


def test_sqlite_accepts_valid_update(sqlite_session):
    sqlite_session.execute(
        text(
            "UPDATE population SET reference_period_end = :value "
            "WHERE rowid = (SELECT min(rowid) FROM population)"
        ),
        {"value": "2030-12-31 23:59:59.999999"},
    )
    sqlite_session.rollback()
