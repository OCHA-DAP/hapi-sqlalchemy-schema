from sqlalchemy.schema import CheckConstraint

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


def reference_period_constraint() -> CheckConstraint:
    """reference_period_end should be greater than reference_period_start"""
    sqltext = "reference_period_end >= reference_period_start "
    return CheckConstraint(sqltext=sqltext, name="reference_period")
