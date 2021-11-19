from enum import Enum, unique, auto


class StrEnum(str, Enum):
    def _generate_next_value_(name, *_):
        return name.upper()


@unique
class Rarity(StrEnum):
    """
    GRAY -> COMMON
    LIGHT BLUE -> UNCOMMON
    BLUE -> RARE
    PURPLE -> MYTHICAL
    PINK -> LEGENDARY
    RED -> ANCIENT
    YELLOW -> CONTRABAND (HOWL / HOWL STICKER)
    """

    COMMON = auto()
    UNCOMMON = auto()
    LEGENDARY = auto()
    RARE = auto()
    MYTHICAL = auto()
    ANCIENT = auto()
    CONTRABAND = auto()
