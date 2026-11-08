"""SQLite-only DDL and engine settings so that SQLite rejects the values
Postgres rejects. Postgres DDL is unaffected.

HAPI tables are created as STRICT tables, with these column CHECKs:

- String(n): length(col) <= n, no NUL characters
- Enum: col IN (values)
- Boolean: col IN (0, 1)
- Integer: 32-bit range (SmallInteger: 16-bit)
- DateTime/Date: a valid date that SQLite doesn't normalise (2024-02-30 is
  rejected, not stored as 2024-03-01)

Foreign keys and NaN need engine settings: call configure_sqlite_engine.
"""

import math
from collections.abc import Mapping
from typing import Any, List, Tuple

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    Engine,
    Enum,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Table,
    TypeDecorator,
    event,
)
from sqlalchemy.exc import CompileError
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import CreateColumn, CreateTable
from sqlalchemy.sql.compiler import DDLCompiler

_INT_RANGES = {
    Integer: (-(2**31), 2**31 - 1),
    SmallInteger: (-(2**15), 2**15 - 1),
}


def _is_hapi_table(table: Table) -> bool:
    # Imported here because utils.base imports this module
    from hapi_schema.utils.base import Base

    return table.metadata is Base.metadata


def _strict_type_and_checks(column: Column, name: str) -> Tuple[str, List[str]]:
    """Return the STRICT type name and the CHECK expressions for a column"""
    col_type = column.type
    while isinstance(col_type, TypeDecorator):
        col_type = col_type.impl_instance

    if isinstance(col_type, Enum):
        values = ", ".join(
            "'" + value.replace("'", "''") + "'" for value in col_type.enums
        )
        return "TEXT", [f"{name} IN ({values})"]
    if isinstance(col_type, String):
        checks = [f"instr({name}, char(0)) = 0"]
        if col_type.length:
            checks.append(f"length({name}) <= {col_type.length}")
        return "TEXT", checks
    if isinstance(col_type, Boolean):
        return "INTEGER", [f"{name} IN (0, 1)"]
    if isinstance(col_type, BigInteger):
        return "INTEGER", []
    if isinstance(col_type, Integer):
        int_type = SmallInteger if isinstance(col_type, SmallInteger) else Integer
        low, high = _INT_RANGES[int_type]
        return "INTEGER", [f"{name} BETWEEN {low} AND {high}"]
    if isinstance(col_type, Numeric):  # Includes Float
        return "REAL", []
    if isinstance(col_type, DateTime):
        # date() of the full value rounds 23:59:59.999999 up to the next day
        day = f"substr({name}, 1, 10)"
        return "TEXT", [
            f"{name} IS NULL OR (datetime({name}) IS NOT NULL AND date({day}) IS {day})"
        ]
    if isinstance(col_type, Date):
        return "TEXT", [f"{name} IS NULL OR date({name}) IS {name}"]
    return "ANY", []


@compiles(CreateColumn, "sqlite")
def _create_column(element: CreateColumn, compiler: DDLCompiler, **kw: Any) -> str:
    text = compiler.visit_create_column(element, **kw)
    column = element.element
    if text is None or not _is_hapi_table(column.table):
        return text
    name = compiler.preparer.format_column(column)
    col_type = compiler.dialect.type_compiler_instance.process(
        column.type, type_expression=column
    )
    prefix = f"{name} {col_type}"
    if not text.startswith(prefix):
        raise CompileError(f"Unexpected SQLite column DDL: {text}")
    strict_type, checks = _strict_type_and_checks(column, name)
    text = f"{name} {strict_type}{text[len(prefix) :]}"
    for check in checks:
        text += f" CHECK ({check})"
    return text


@compiles(CreateTable, "sqlite")
def _create_table(element: CreateTable, compiler: DDLCompiler, **kw: Any) -> str:
    text = compiler.visit_create_table(element, **kw)
    table = element.element
    options = table.dialect_options["sqlite"]
    if not _is_hapi_table(table) or options["strict"]:
        return text
    version = compiler.dialect.server_version_info  # None until connected
    if version and version < (3, 37):
        raise CompileError(
            f"SQLite {'.'.join(map(str, version))} lacks STRICT tables (3.37+)"
        )
    separator = " " if options["with_rowid"] else ", "
    return f"{text.rstrip()}{separator}STRICT\n\n"


def _reject_nan(parameters: Any) -> None:
    values = parameters.values() if isinstance(parameters, Mapping) else parameters
    for value in values or ():
        if isinstance(value, float) and math.isnan(value):
            raise ValueError("NaN is not supported: SQLite would store it as NULL")


def configure_sqlite_engine(engine: Engine) -> None:
    """Enable foreign keys on each connection and reject NaN parameters, which
    SQLite would otherwise store as NULL. Call before the engine first
    connects."""

    @event.listens_for(engine, "connect")
    def _enable_foreign_keys(dbapi_connection: Any, _: Any) -> None:
        dbapi_connection.execute("PRAGMA foreign_keys=ON")

    @event.listens_for(engine, "before_cursor_execute")
    def _check_parameters(
        _conn: Any,
        _cursor: Any,
        _statement: str,
        parameters: Any,
        _context: Any,
        executemany: bool,
    ) -> None:
        if executemany:
            for row in parameters:
                _reject_nan(row)
        else:
            _reject_nan(parameters)
