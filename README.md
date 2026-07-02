# hapi-sqlalchemy-schema

Schema for HAPI database in SQLAlchemy

## Installation

```bash
pip install hapi-schema
```

With database utilities:
```bash
pip install hapi-schema[database]
```

## Development

Install [uv](https://docs.astral.sh/uv/), then:

```bash
uv sync --all-groups
uv run pytest
```
