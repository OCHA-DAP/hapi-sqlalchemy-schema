from datetime import datetime

data_admin1 = [
    dict(
        location_ref=1,
        code="FOO-XXX",
        name="Unspecified",
        is_unspecified=True,
        reference_period_start=None,
        reference_period_end=None,
        hapi_updated_date=datetime(2023, 1, 1),
        hapi_replaced_date=None,
    ),
    dict(
        location_ref=1,
        code="FOO-001",
        name="Province 01",
        is_unspecified=False,
        reference_period_start=None,
        reference_period_end=None,
        hapi_updated_date=datetime(2023, 1, 1),
        hapi_replaced_date=None,
    ),
    dict(
        location_ref=1,
        code="FOO-002",
        name="Province 02",
        is_unspecified=False,
        reference_period_start=None,
        reference_period_end=None,
        hapi_updated_date=datetime(2023, 1, 1),
        hapi_replaced_date=None,
    ),
]
