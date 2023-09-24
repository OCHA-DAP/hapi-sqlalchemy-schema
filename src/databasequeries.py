"""Functions that perform queries of the HAPI database
"""
import logging
from datetime import datetime

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class DatabaseQueries:
    """A class that offers functions that query the HAPI database

    Args:
        session (sqlalchemy.orm.Session): Session to use for queries
        now (datetime): Date to use for now
    """

    def __init__(self, session: Session, now: datetime):
        self.session = session
        self.now = now

    # FIXME: remove
    # Functions below are illustrative (and copied from freshness) not useful for this project
    #
    #  Not real function we would use but a reminder of SQLAlchemy syntax
    # def get_number_datasets(self) -> Tuple[int, int]:
    #     """Get the number of datasets today and yesterday in a tuple
    #
    #     Returns:
    #          Tuple[int, int]: (number of datasets today, number of datasets yesterday)
    #     """
    #     datasets_today = self.session.execute(
    #         select(func.count(DBDataset.id)).where(
    #             DBDataset.run_number == self.run_numbers[0][0]
    #         )
    #     ).scalar_one()
    #     datasets_previous = self.session.execute(
    #         select(func.count(DBDataset.id)).where(
    #             DBDataset.run_number == self.run_numbers[1][0]
    #         )
    #     ).scalar_one()
    #     return datasets_today, datasets_previous

    # FIXME: remove
    #  Not real function we would use but a reminder of SQLAlchemy syntax
    # def get_broken(self) -> Dict[str, Dict]:
    #     """Get dateset information categorised by error message
    #
    #     Returns:
    #          Dict[str, Dict]: Dataset information categorised by error message
    #     """
    #     columns = [
    #         DBResource.id.label("resource_id"),
    #         DBResource.name.label("resource_name"),
    #         DBResource.dataset_id.label("id"),
    #         DBResource.error,
    #         DBInfoDataset.name,
    #         DBInfoDataset.title,
    #         DBInfoDataset.maintainer,
    #         DBOrganization.id.label("organization_id"),
    #         DBOrganization.title.label("organization_title"),
    #         DBDataset.update_frequency,
    #         DBDataset.latest_of_modifieds,
    #         DBDataset.what_updated,
    #         DBDataset.fresh,
    #     ]
    #     filters = [
    #         DBResource.dataset_id == DBInfoDataset.id,
    #         DBInfoDataset.organization_id == DBOrganization.id,
    #         DBResource.dataset_id == DBDataset.id,
    #         DBDataset.run_number == self.run_numbers[0][0],
    #         DBResource.run_number == DBDataset.run_number,
    #         DBResource.error.is_not(None),
    #         DBResource.when_checked > self.run_numbers[1][1],
    #     ]
    #     results = self.session.execute(select(*columns).where(*filters))
    #     norows = 0
    #     for norows, result in enumerate(results):
    #         row = dict()
    #         for i, column in enumerate(columns):
    #             row[column.key] = result[i]
    #         error = row["error"]
