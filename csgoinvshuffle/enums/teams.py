from enum import unique, IntEnum

@unique
class TeamSide(IntEnum):
    BOTH = 0
    T = 1
    CT = 2