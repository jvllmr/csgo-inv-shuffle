from __future__ import annotations
from typing import Iterator, Optional, SupportsIndex
from csgoinvshuffle.enums.filters_enums import TagsInternalName
import requests
from csgoinvshuffle.exceptions import InventoryIsPrivateException, TooManyRequestsAtOnce
from csgoinvshuffle.item import Item
from enum import Enum, EnumMeta


class NotAnItemError(TypeError):
    """Something wasn't an item"""

    def __init__(self, item, *args, **kwargs):
        super().__init__(f"{str(type(item))} is not an Item", *args, **kwargs)


class Inventory(list):
    """
    Represents a CS:GO Inventory
    """

    owner_id: str

    def __init__(
        self, *items: Item, assets=None, descriptions=None, steamid64: str = None
    ):
        if assets and descriptions and steamid64:
            self.owner_id = steamid64
            assets = iter(assets)
            descriptions = iter(descriptions)
            try:
                while True:
                    self.append(
                        Item(next(descriptions), next(assets), steamid64=steamid64)
                    )
            except StopIteration:
                return
        else:
            for item in items:
                self.append(item)

    def __iter__(self) -> Iterator[Item]:  # type: ignore
        return super().__iter__()

    def __getitem__(self, i: SupportsIndex) -> Item:  # type: ignore
        return super().__getitem__(i)

    def append(self, item: Item):
        if not isinstance(item, Item):
            raise NotAnItemError(item)
        return super().append(item)

    def __repr__(self):
        return str(list(self))

    def __str__(self):
        return str(list(map(lambda item: str(item), self)))

    def filter(self, value: Enum, filter_by: EnumMeta = TagsInternalName) -> Inventory:
        """Filter the inventory by a special property"""

        if not isinstance(filter_by, EnumMeta):
            raise TypeError("filter_by argument needs to be an EnumMeta")

        value = value if not isinstance(value, Enum) else value.value

        if filter_by == TagsInternalName:

            def filter_(x):
                return value in [t["internal_name"] for t in x.tags]

        else:
            raise ValueError("Filter for that enum isn't implemented")

        return Inventory(*filter(filter_, self))


def parse_inventory(json: dict, steamid64: str) -> Inventory:
    """Parses an inventory from a json"""

    inv = Inventory(
        assets=json["assets"], descriptions=json["descriptions"], steamid64=steamid64
    )

    return inv


def get_inventory(steamid64: str) -> Optional[Inventory]:
    """
    Get the CS:GO Inventory of a steam user by his 64-bit ID

    The Inventory has to be public
    """
    if not steamid64:
        return None
    r = requests.get(f"https://steamcommunity.com/inventory/{steamid64}/730/2")

    if r.status_code == 200:
        json = r.json()
        if not json.get("success"):
            raise requests.HTTPError(json.get("Error"))
        return parse_inventory(json, steamid64)
    elif r.status_code == 403:
        raise InventoryIsPrivateException("The requested Inventory is private.")
    elif r.status_code == 500:
        raise TooManyRequestsAtOnce(
            "Too many requests at once. Please try again in few seconds."
        )
    else:
        raise requests.HTTPError(f"Steam returned status code {r.status_code}")
