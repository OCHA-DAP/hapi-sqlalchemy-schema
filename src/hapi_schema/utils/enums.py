from enum import Enum as PythonEnum
from typing import List, Type

from sqlalchemy import Enum as SQLAlchemyEnum

"""The two functions below create enums using the values rather than the keys"""


def _get_list_of_values(enum_class: Type[PythonEnum]) -> List[str]:
    return [e.value for e in enum_class]


def build_enum_using_values(enum_class: Type[PythonEnum]) -> SQLAlchemyEnum:
    return SQLAlchemyEnum(enum_class, values_callable=_get_list_of_values)


class Gender(str, PythonEnum):
    FEMALE = "f"
    MALE = "m"
    NONBINARY = "x"
    UNSPECIFIED = "u"
    OTHER = "o"
    ALL = "all"


class DisabledMarker(str, PythonEnum):
    YES = "y"
    NO = "n"
    ALL = "all"


class EventType(str, PythonEnum):
    CIVILIAN_TARGETING = "civilian_targeting"
    DEMONSTRATION = "demonstration"
    POLITICAL_VIOLENCE = "political_violence"


class PopulationGroup(str, PythonEnum):
    REFUGEES = "REF"
    ROC = "ROC"
    ASYLUM_SEEKERS = "ASY"
    OIP = "OIP"
    IDP = "IDP"
    IOC = "IOC"
    STATELESS = "STA"
    OOC = "OOC"
    HOST_COMMUNITY = "HST"
    RET = "RET"
    RESETTLED = "RST"
    NATURALIZED = "NAT"
    RDP = "RDP"
    RRI = "RRI"
    ALL = "all"


class PopulationStatus(str, PythonEnum):
    AFFECTED = "AFF"
    INNEED = "INN"
    TARGETED = "TGT"
    REACHED = "REA"
    ALL = "all"


class PriceFlag(str, PythonEnum):
    ACTUAL = "actual"
    AGGREGATE = "aggregate"
    ACTUAL_AGGREGATE = "actual,aggregate"


class PriceType(str, PythonEnum):
    FARM_GATE = "Farm Gate"
    RETAIL = "Retail"
    WHOLESALE = "Wholesale"


class IPCPhase(str, PythonEnum):
    PHASE_1 = "1"
    PHASE_2 = "2"
    PHASE_3 = "3"
    PHASE_4 = "4"
    PHASE_5 = "5"
    PHASE_3_PLUS = "3+"
    ALL = "all"


class IPCType(str, PythonEnum):
    CURRENT = "current"
    FIRST_PROJECTION = "first projection"
    SECOND_PROJECTION = "second projection"


class RiskClass(str, PythonEnum):
    VERY_LOW = "1"
    LOW = "2"
    MEDIUM = "3"
    HIGH = "4"
    VERY_HIGH = "5"


class CommodityCategory(str, PythonEnum):
    CEREALS_TUBERS = "cereals and tubers"
    MEAT_FISH_EGGS = "meat, fish and eggs"
    MILK_DAIRY = "milk and dairy"
    MISCELLANEOUS_FOOD = "miscellaneous food"
    NON_FOOD = "non-food"
    OIL_FATS = "oil and fats"
    PULSES_NUTS = "pulses and nuts"
    VEGETABLES_FRUITS = "vegetables and fruits"
