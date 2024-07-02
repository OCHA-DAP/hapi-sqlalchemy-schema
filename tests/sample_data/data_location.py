from datetime import datetime

data_location = [
    dict(
        code="FOO",
        name="Foolandia",
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=None,
    ),
    dict(
        code="BAR",
        name="Barovia",
        has_hno=False,
        in_gho=True,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=None,
        from_cods=False,
    ),
]
