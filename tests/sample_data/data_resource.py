from datetime import datetime

data_resource = [
    dict(
        id=1,
        dataset_ref=1,
        hdx_id="90deb235-1bf5-4bae-b231-3393222c2d01",
        name="resource-01.csv",
        format="csv",
        update_date=datetime(2023, 6, 1),
        download_url="https://data.humdata.org/dataset/c3f001fa-b45b-464c-9460-1ca79fd39b40/resource/90deb235-1bf5-4bae-b231-3393222c2d01/download/resource-01.csv",
        is_hxl=True,
    ),
    dict(
        id=2,
        dataset_ref=1,
        hdx_id="b9e438e0-b68a-49f9-b9a9-68c0f3e93604",
        name="resource-02.xlsx",
        format="xlsx",
        update_date=datetime(2023, 7, 1),
        download_url="https://fdw.fews.net/api/tradeflowquantityvaluefacts/?dataset=1845&country=TZ&fields=simple&format=xlsx",
        is_hxl=True,
    ),
    dict(
        id=3,
        dataset_ref=2,
        hdx_id="62ad6e55-5f5d-4494-854c-4110687e9e25",
        name="resource-03.csv",
        format="csv",
        update_date=datetime(2023, 8, 1),
        download_url="https://data.humdata.org/dataset/7cf3cec8-dbbc-4c96-9762-1464cd0bff75/resource/62ad6e55-5f5d-4494-854c-4110687e9e25/download/resource-03.csv",
        is_hxl=True,
    ),
]
