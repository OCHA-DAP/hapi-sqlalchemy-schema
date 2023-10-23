# Taken from page 53 of
# https://www.ipcinfo.org/fileadmin/user_upload/ipcinfo/manual/IPC_Technical_Manual_3_Final.pdf
data_ipc_phase = [
    dict(
        code="1",
        name="Phase 1: None/Minimal",
        description="Households are able to meet essential food and non-food "
        "needs without engaging in atypical and unsustainable strategies to "
        "access food and income.",
    ),
    dict(
        code="2",
        name="Phase 2: Stressed",
        description="Households have minimally adequate food consumption but "
        "are unable to afford some essential non-food expenditures without "
        "engaging in stress-coping strategies.",
    ),
    dict(
        code="3",
        name="Phase 3: Crisis",
        description="Households either have food consumption gaps that are "
        "reflected by high or above-usual acute malnutrition, or are "
        "marginally able to meet minimum food needs but only by depleting "
        "essential livelihood assets or through crisis-coping strategies.",
    ),
    dict(
        code="3+",
        name="Phase 3+: In Need of Action",
        description="Sum of population in phases 3, 4, and 5. The population "
        "in Phase 3+ does not necessarily reflect the full population in need "
        "of urgent action. This is because some households may be in Phase 2 "
        "or even 1 but only because of receipt of assistance, and thus, they "
        "may be in need of continued action.",
    ),
]
