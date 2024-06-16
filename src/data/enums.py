from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3