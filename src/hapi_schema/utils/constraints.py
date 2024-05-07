from sqlalchemy.schema import CheckConstraint, UniqueConstraint

# TODO: should these remain as functions or just be turned into variables?
#  Functions could be handy in case of future need for parameterization


def min_age_constraint() -> CheckConstraint:
    """If the age range is rolled up, min_age should be NULL.
    Otherwise, it should be in integer of 0 or greater."""
    sqltext = "(age_range = '*' AND min_age IS NULL) OR (age_range != '*' AND min_age >= 0)"
    return CheckConstraint(sqltext=sqltext, name="min_age_constraint")


def max_age_constraint() -> CheckConstraint:
    """If the age range is rolled up, min_age will be NULL and
    max_age should also be null. Otherwise, min_age will be an integer,
    and max age should be equal to or greater, or NULL."""
    # TODO: can this logic be simplified a bit?
    sqltext = "(min_age IS NULL AND max_age IS NULL) OR (min_age IS NOT NULL AND (max_age is NULL OR max_age >= min_age))"
    return CheckConstraint(sqltext=sqltext, name="max_age_constraint")


def populateion_constraint() -> CheckConstraint:
    """Population must not be a negative number."""
    sqltext = "population >= 0"
    return CheckConstraint(sqltext=sqltext, name="population_constraint")


def reference_period_constraint() -> CheckConstraint:
    """reference_period_end should be greater than reference_period_start"""
    sqltext = "reference_period_end >= reference_period_start "
    return CheckConstraint(sqltext=sqltext, name="reference_period")


def general_risk_constraint(risk_name: str) -> CheckConstraint:
    sqltext = f"({risk_name}_risk >= 0) AND ({risk_name}_risk <= 10)"
    return CheckConstraint(sqltext=sqltext, name=f"{risk_name}_risk")


def code_and_reference_period_unique_constraint(
    admin_level: str,
) -> UniqueConstraint:
    return UniqueConstraint(
        "code",
        "reference_period_start",
        name=f"{admin_level}_code_and_reference_period_unique",
    )
