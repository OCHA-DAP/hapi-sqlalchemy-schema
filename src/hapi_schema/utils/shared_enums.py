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
    IDPS = "IDP"
    IOC = "IOC"
    STATELESS_PEOPLE = "STA"
    OOC = "OOC"
    HOST_COMMUNITY = "HST"

