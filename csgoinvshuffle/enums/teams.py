from enum import unique, IntEnum, auto


@unique
class TeamSide(IntEnum):
    BOTH = auto()
    T = auto()
    CT = auto()
