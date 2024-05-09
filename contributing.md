# Development

## Environment

Development is currently done using Python 3.11. We recommend using a virtual
environment such as ``venv``:

    python3.11 -m venv venv
    source venv/bin/activate

In your virtual environment, please install all packages for
development by running:

    pip install -r requirements.txt

and then make an editable installation of the package:

    pip install -e .

## Pre-Commit

Also be sure to install `pre-commit`, which is run every time
you make a git commit:

    pre-commit install

The configuration file for this project is in a
non-standard location. Thus, you will need to edit your
`.git/hooks/pre-commit` file to reflect this. Change
the line that begins with `ARGS` to:

    ARGS=(hook-impl --config=.config/pre-commit-config.yaml --hook-type=pre-commit)

With pre-commit, all code is formatted according to
[ruff]("https://github.com/charliermarsh/ruff") guidelines.

To check if your changes pass pre-commit without committing, run:

    pre-commit run --all-files --config=.config/pre-commit-config.yaml

## Testing

Testing is now done against a Postgres database which can be deployed from the Docker definition in the `docker` directory using:

`docker-compose up -d`

To run the tests and view coverage, execute:

    pytest -c .config/pytest.ini --cov hapi_schema --cov-config .config/coveragerc

Follow the example set out already in ``documentation/main.md`` as you write the documentation.

## Packages

[pip-tools](https://github.com/jazzband/pip-tools) is used for
package management.  If you’ve introduced a new package to the
source code (i.e.anywhere in `src/`), please add it to the
`project.dependencies` section of
`pyproject.toml` with any known version constraints.

For adding packages for testing or development, add them to
the `test` or `dev` sections under `[project.optional-dependencies]`.

Any changes to the dependencies will be automatically reflected in
`requirements.txt` with `pre-commit`, but you can re-generate
the file without committing by executing:

    pre-commit run pip-compile --all-files --config=.config/pre-commit-config.yaml

## Adding a new table

To add a new table to the schema:

1. Add a `db_[table_name].py` file to `src/hapi_schema` which implements the table as a class derived from `hapi_schema.utils.base.Base`
2. Add a file `data_[table_name].py` to `tests/sample_data` which contains three rows of data for the new table as a list of dictionaries.
3. Add the table to the `tests/conftest.py` with an import like:
   `from sample_data.data_[table_name] import data_[table_name]`
   and data inserted with:
   `session.execute(insert(DBPatch), data_patch)`
4. Add a test file for the new table as `tests/test_[table_name].py`
