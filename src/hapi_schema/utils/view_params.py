from dataclasses import dataclass

from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.sql.expression import Selectable


@dataclass
class ViewParams:
    """Class for keeping view constructor parameters."""

    name: str
    metadata: DeclarativeMeta
    selectable: Selectable
