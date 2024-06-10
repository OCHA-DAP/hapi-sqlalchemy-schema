from datetime import datetime

data_location = [
    dict(
        id=1,
        code="FOO",
        name="Foolandia",
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=None,
    ),
    dict(
        id=2,
        code="BAR",
        name="Barovia",
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=None,
        from_cods=False,
    ),
]
