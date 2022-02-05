import typing as t

from typing_extensions import TypedDict

from csgoinvshuffle.enums.filters_enums import TagsInternalName
from csgoinvshuffle.enums.loadout_slots import LoadoutSlot


class Description(TypedDict):
    type: str
    value: str
    color: str


class Action(TypedDict):
    name: str
    link: str


class MarketAction(TypedDict):
    name: str
    link: str


class Tag(TypedDict):
    internal_name: str
    name: str
    category: str
    category_name: str


class Sticker(TypedDict):
    name: str
    link: str


SlotTagMap = t.Dict[LoadoutSlot, t.Tuple[TagsInternalName, ...]]
