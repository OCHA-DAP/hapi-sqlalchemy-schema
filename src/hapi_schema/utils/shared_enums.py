import enum


class Gender(str, enum.Enum):
    FEMALE = "f"
    MALE = "m"
    NONBINARY = "x"


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


class PopulationStatus(str, enum.Enum):
    POPULATION = "POP"
    AFFECTED = "AFF"
    INNEED = "INN"
    TARGETED = "TGT"
    REACHED = "REA"
