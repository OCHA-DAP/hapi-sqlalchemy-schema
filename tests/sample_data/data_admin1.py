from datetime import datetime

data_admin1 = [
    dict(
        id=1,
        location_ref=1,
        code="FOO-XXX",
        name="Unspecified",
        is_unspecified=True,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=None,
    ),
    dict(
        id=2,
        location_ref=1,
        code="FOO-001",
        name="Province 01",
        is_unspecified=False,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=None,
    ),
    dict(
        id=3,
        location_ref=1,
        code="FOO-002",
        name="Province 02",
        is_unspecified=False,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=None,
    ),
]
