from datetime import datetime

data_food_security = [
    # Phase 1 current national
    dict(
        id=1,
        resource_ref=3,
        admin2_ref=1,
        ipc_phase_code=1,
        ipc_type_code=1,
        population_total=1_000_000,
        population_in_phase=500_000,
        population_fraction_in_phase=0.5,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 3, 30),
        source_data="DATA,DATA,DATA",
    ),
    # Phase 2 first projection admin1
    dict(
        id=2,
        resource_ref=3,
        admin2_ref=2,
        ipc_phase_code=2,
        ipc_type_code=2,
        population_total=100_000,
        population_in_phase=40_000,
        population_fraction_in_phase=0.4,
        reference_period_start=datetime(2023, 4, 1),
        reference_period_end=datetime(2023, 6, 30),
        source_data="DATA,DATA,DATA",
    ),
    # Phase 3 second projection admin2
    dict(
        id=3,
        resource_ref=3,
        admin2_ref=4,
        ipc_phase_code=3,
        ipc_type_code=3,
        population_total=10_000,
        population_in_phase=3_000,
        population_fraction_in_phase=0.3,
        reference_period_start=datetime(2023, 7, 1),
        reference_period_end=datetime(2023, 10, 31),
        source_data="DATA,DATA,DATA",
    ),
]
