from csgoinvshuffle.enums.filters_enums import TagsInternalName
import requests
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
    def __init__(self, *items):
        for item in items:
            self.append(item)
            
    def append(self, item: Item):
        if not isinstance(item, Item):
            raise NotAnItemError(item)
        return super().append(item)
    
    def __repr__(self):
        return str(list(self))

    def __str__(self):
        return str(list(map(lambda item: str(item), self)))
    
    def filter(self, value: Enum, filter_by: EnumMeta=TagsInternalName):
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

    inv = Inventory()
    setattr(inv, "owner_id", steamid64)
    for attributes in json["rgInventory"].values():
        item = Item()
        for key, value in attributes.items():
            setattr(item, key, value)
        
        for key, value in json["rgDescriptions"][f"{item.classid}_{item.instanceid}"].items():
            # We create the actual inspect link for every item
            if key == "actions" or key == "market_actions":
                json["rgDescriptions"][f"{item.classid}_{item.instanceid}"][key][0]["link"] = json["rgDescriptions"][f"{item.classid}_{item.instanceid}"][key][0]["link"].replace(
                    r"%assetid%", str(item.id)
                ).replace(r"%20M%listingid%", f" S{steamid64}")
            setattr(item, key, value)

        inv.append(item)
        del item

    return inv
    

def get_inventory(steamid64: str) -> Inventory:
    """
    Get the CS:GO Inventory of a steam user by his 64-bit ID

    The Inventory has to be public
    """
    if not steamid64:
        return None
    r = requests.get(f"https://steamcommunity.com/profiles/{steamid64}/inventory/json/730/2")

    if r.status_code == 200:
        return parse_inventory(r.json(), steamid64)
    elif r.status_code == 429:
        raise requests.HTTPError("Too many requests at once. Please try again in a minute.")
    else:
        raise requests.HTTPError(f"Steam returned status code {r.status_code}")
