from enum import IntEnum, auto, unique


@unique
class TeamSide(IntEnum):
    BOTH = auto()
    T = auto()
    CT = auto()
