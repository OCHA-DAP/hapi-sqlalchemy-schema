from sqlalchemy.schema import CheckConstraint, UniqueConstraint

# TODO: should these remain as functions or just be turned into variables?
#  Functions could be handy in case of future need for parameterization


def min_age_constraint() -> CheckConstraint:
    """If the age range is rolled up, min_age should be NULL.
    Otherwise, it can be NULL for unknown, or should be an
    integer of 0 or greater."""
    sqltext = (
        "(age_range = 'all' AND min_age IS NULL) OR "
        "(age_range != 'all' AND min_age >= 0)"
    )
    return CheckConstraint(sqltext=sqltext, name="min_age_constraint")


def max_age_constraint() -> CheckConstraint:
    """If min_age is NULL, max age should also be NULL.
    Otherwise, when min_age is an integer, max age should be equal to
    or greater, or NULL."""
    # TODO: can this logic be simplified a bit?
    sqltext = (
        "(min_age IS NULL AND max_age IS NULL) OR "
        "(min_age IS NOT NULL AND (max_age is NULL OR max_age >= min_age))"
    )
    return CheckConstraint(sqltext=sqltext, name="max_age_constraint")


def population_constraint(
    population_var_name: str = "population",
) -> CheckConstraint:
    """Population must not be a negative number."""
    sqltext = f"{population_var_name} >= 0"
    return CheckConstraint(
        sqltext=sqltext, name=f"{population_var_name}_constraint"
    )


def non_negative_constraint(
    var_name: str,
) -> CheckConstraint:
    """Require a column to be non-negative."""
    sqltext = f"{var_name} >= 0"
    return CheckConstraint(sqltext=sqltext, name=f"{var_name}_constraint")


def percentage_constraint(var_name: str) -> CheckConstraint:
    sqltext = f"{var_name} >= 0. AND {var_name} <= 100."
    return CheckConstraint(sqltext=sqltext, name=f"{var_name}_constraint")


def reference_period_constraint() -> CheckConstraint:
    """reference_period_end should be greater than reference_period_start"""
    sqltext = "reference_period_end >= reference_period_start "
    return CheckConstraint(sqltext=sqltext, name="reference_period_constraint")


def general_risk_constraint(risk_name: str) -> CheckConstraint:
    sqltext = f"({risk_name}_risk >= 0) AND ({risk_name}_risk <= 10)"
    return CheckConstraint(
        sqltext=sqltext, name=f"{risk_name}_risk_constraint"
    )


def code_and_reference_period_unique_constraint(
    admin_level: str,
) -> UniqueConstraint:
    return UniqueConstraint(
        "code",
        "reference_period_start",
        name=f"{admin_level}_code_and_reference_period_unique_constraint",
    )


def latlon_constraint() -> CheckConstraint:
    """Latitude and longitude must be valid"""
    sqltext = "lat <= 90.0 AND lat >= -90.0 AND lon <= 180.0 AND lon >= -180.0"
    return CheckConstraint(sqltext=sqltext, name="latlon_constraint")
