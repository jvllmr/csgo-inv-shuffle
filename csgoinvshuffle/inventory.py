import requests
from .item import Item
from enum import Enum

class Inventory(list):

    def __init__(self, *args):
        super().__init__(args)
        for item in args:
            if isinstance(item, list):
                if isinstance(item, Inventory):
                    self.owner_id = item.owner_id
                    
                for subitem in item:
                    self.append(subitem)  
                self.remove(item)
            else:
                self.__add_filters(item)

    def append(self, item: Item):
        if not isinstance(item, Item):
            raise TypeError(f"{str(type(item))} is not an Item")
        self.__add_filters(item)
        return super().append(item)
    
    def __repr__(self):
        return str(list(self))

    def __str__(self):
        return str(list(map(lambda item: str(item), self)))
    

    def __add_filters(self, item: Item) -> None:
        """
        Adds the filters for item attributes
        """
        for attr in dir(item):
            if not attr.startswith("_"):

                attr_value = getattr(item, attr)
                if type(attr_value) == list:
                    
                    for entry in attr_value:
                        """
                        This was originally used for the custom name tag filter

                        if type(entry) == str:
                            function_name= f"filter_by_{attr}_{entry.split(':')[0].replace(' ','_').lower()}"
                            if not getattr(self, function_name, ""):
                                setattr(self, function_name, lambda s, attr=attr: Inventory([x for x in self if str(s) in str(getattr(x,attr)[0])]))
                        """
                        if type(entry) == dict:
                            for key in entry.keys():
                                if not getattr(self, f"filter_by_{attr}_{key}", ""):
                                    setattr(self, f"filter_by_{attr}_{key}", lambda s , attr=attr, key=key: Inventory([x for x in self for d in getattr(x,attr) if str(getattr(s, "value", s)) in str(d[key])]))
                else:
                    if not getattr(self, f"filter_by_{attr}", ""):
                        setattr(self, f"filter_by_{attr}", lambda s, attr=attr: Inventory([x for x in self if str(getattr(s, "value", s)) in str(getattr(x, attr))]))

def __parse_inventory(json: dict, steamid64: str) -> Inventory:
    inv = Inventory()
    setattr(inv, "owner_id" , steamid64)
    for attributes in json["rgInventory"].values():
        item = Item()
        for key, value in attributes.items():
            setattr(item, key, value)
        
        for key, value in json["rgDescriptions"][f"{item.classid}_{item.instanceid}"].items():
            # We create the actual inspect link for every item
            if key == "actions" or key == "market_actions":
                json["rgDescriptions"][f"{item.classid}_{item.instanceid}"][key][0]["link"] = json["rgDescriptions"][f"{item.classid}_{item.instanceid}"][key][0]["link"].replace(r"%assetid%", str(item.id)).replace(r"%20M%listingid%",f" S{steamid64}")
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
        return __parse_inventory(r.json(), steamid64)
    elif r.status_code == 429:
        raise requests.HTTPError(f"Too many requests at once. Please try again in a minute.")
    else:
        raise requests.HTTPError(f"Steam returned status code {r.status_code}")