from dataclasses import dataclass

from sqlalchemy.sql.expression import Selectable
from sqlalchemy.sql.schema import MetaData


@dataclass
class ViewParams:
    """Class for keeping view constructor parameters."""

    name: str
    metadata: MetaData
    selectable: Selectable
