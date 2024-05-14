from datetime import datetime

data_food_security = [
    # Phase 1 current national
    dict(
        resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
        admin2_ref=1,
        ipc_phase="1",
        ipc_type="current",
        population_in_phase=500_000,
        population_fraction_in_phase=0.5,
        reference_period_start=datetime(2023, 1, 1),
        reference_period_end=datetime(2023, 3, 30),
    ),
    # Phase 2 first projection admin1
    dict(
        resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
        admin2_ref=2,
        ipc_phase="2",
        ipc_type="first projection",
        population_in_phase=40_000,
        population_fraction_in_phase=0.4,
        reference_period_start=datetime(2023, 4, 1),
        reference_period_end=datetime(2023, 6, 30),
    ),
    # Phase 3 second projection admin2
    dict(
        resource_hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
        admin2_ref=4,
        ipc_phase="3",
        ipc_type="second projection",
        population_in_phase=3_000,
        population_fraction_in_phase=0.3,
        reference_period_start=datetime(2023, 7, 1),
        reference_period_end=datetime(2023, 10, 31),
    ),
]
