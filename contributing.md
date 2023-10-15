# Development

## Environment

Development is currently done using Python 3.11. We recommend using a virtual
environment such as ``venv``:

    python3.11 -m venv venv
    source venv/bin/activate

In your virtual environment, please install all packages for
development by running:

    pip install -r requirements.txt

## Testing

To run the tests and view coverage, execute:

    pytest -c .config/pytest.ini --cov hapi_schema --cov-config .config/coveragerc


## Pre-Commit

Also be sure to install `pre-commit`, which is run every time
you make a git commit:

    pre-commit install

The configuration file for this project is in a
non-start location. Thus, you will need to edit your
`.git/hooks/pre-commit` file to reflect this. Change
the line that begins with `ARGS` to:

    ARGS=(hook-impl --config=.config/pre-commit-config.yaml --hook-type=pre-commit)

With pre-commit, all code is formatted according to
[black]("https://github.com/psf/black") and
[ruff]("https://github.com/charliermarsh/ruff") guidelines.

To check if your changes pass pre-commit without committing, run:

    pre-commit run --all-files --config=.config/pre-commit-config.yaml
