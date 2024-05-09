import enum


class Gender(str, enum.Enum):
    FEMALE = "f"
    MALE = "m"
    NONBINARY = "x"
    UNSPECIFIED = "u"
    OTHER = "o"
    EUNUCH = "e"
    ALL = "*"


class DisabledMarker(str, enum.Enum):
    YES = "y"
    NO = "n"
    ALL = "*"


class EventType(str, enum.Enum):
    CIVILIAN_TARGETING = "civilian_targeting"
    DEMONSTRATION = "demonstration"
    POLITICAL_VIOLENCE = "political_violence"


class PopulationGroup(str, enum.Enum):
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
    ALL = "*"


class PopulationStatus(str, enum.Enum):
    POPULATION = "POP"
    AFFECTED = "AFF"
    INNEED = "INN"
    TARGETED = "TGT"
    REACHED = "REA"
    ALL = "*"


class IPCPhase(str, enum.Enum):
    PHASE_1 = "1"
    PHASE_2 = "2"
    PHASE_3 = "3"
    PHASE_4 = "4"
    PHASE_5 = "5"
    PHASE_3_PLUS = "3+"
    ALL = "*"


class IPCType(str, enum.Enum):
    CURRENT = "current"
    FIRST_PROJECTION = "first projection"
    SECOND_PROJECTION = "second projection"


class RiskClass(str, enum.Enum):
    VERY_LOW = "1"
    LOW = "2"
    MEDIUM = "3"
    HIGH = "4"
    VERY_HIGH = "5"
