# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**hapi-sqlalchemy-schema** defines the HAPI (Humanitarian API) database schema using SQLAlchemy ORM models. It is a library published to PyPI that other projects (such as `hapi-pipelines`) import to create and interact with the HAPI PostgreSQL database.

## Commands

Install dependencies:
```bash
uv sync
```

Install with test dependencies:
```bash
uv sync --group test
```

Run tests:
```bash
uv run pytest
```

Run a single test:
```bash
uv run pytest tests/test_location.py
```

Lint check:
```bash
pre-commit run --all-files
```

## Architecture

The library lives under `src/hapi_schema/` and contains:

- **`db_*.py`** — SQLAlchemy ORM table definitions (one file per HAPI data category, e.g. `db_location.py`, `db_funding.py`)
- **`views.py`** — SQLAlchemy view definitions that mirror the tables
- **`utils/`** — shared utilities (e.g. `base.py` with the declarative `Base`)

Tests require a live PostgreSQL instance (`postgresql+psycopg://postgres:postgres@localhost:5432/hapitest`). The `tests/sample_data/` directory holds fixture data used by `conftest.py` to populate the database before tests run.

## Environment

Tests require a running PostgreSQL 14 instance. Use the `docker/docker-compose.yml` to start one locally:
```bash
docker compose -f docker/docker-compose.yml up -d
```

## Collaboration Style

- Be objective, not agreeable. Act as a partner, not a sycophant. Push back when you disagree, flag tradeoffs honestly, and don't sugarcoat problems.
- Keep explanations brief and to the point.
- Don't rely on recalled knowledge for facts that could be stale (API behaviour, library versions, external systems). Search or read the actual source first.

## Scope of Changes

When fixing a bug or addressing PR feedback, change only what is necessary to resolve the specific issue. Do not refactor surrounding code, rename variables, adjust formatting, or make improvements in the same commit unless they are directly required by the fix.
