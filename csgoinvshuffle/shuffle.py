from __future__ import annotations
from csgoinvshuffle.utils import get_depending_item_slots
from csgoinvshuffle.item import Item
from csgoinvshuffle import shuffleformat
from csgoinvshuffle.enums import LoadoutSlot, TeamSide
from functools import cache
from os.path import abspath
from random import random


class ShuffleConfig:
    __slotmap = dict()

    def __init__(self, path: str = "./csgo_saved_item_shuffles.txt"):
        self.path = abspath(path)

        for enum in LoadoutSlot:
            self.__slotmap[enum.value] = dict()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.save()

    def __enter__(self) -> ShuffleConfig:
        return self

    def generate(self) -> str:
        """
        Returns the config content as a string
        """
        ret = shuffleformat.HEADER
        for item_slot in self.__slotmap:
            items = str()
            for cycle_slot, item_id in self.__slotmap[item_slot].items():

                ITEM_ENTRY = shuffleformat.ITEM_ENTRY
                if cycle_slot > 9:
                    ITEM_ENTRY.replace(" ", "")
                items += ITEM_ENTRY.replace("$nr$", str(cycle_slot)).replace(
                    "$item_id$", self.__hex_convert(int(item_id))
                )

            loadoutslot = shuffleformat.SLOT_ENTRY.replace(
                "$id$", str(item_slot)
            ).replace("$item_entries$", items)
            ret += loadoutslot
        return ret + shuffleformat.END

    def save(self):
        """
        Save the config to a file
        """
        with open(self.path, "w") as f:
            f.write(self.generate())

    @cache
    def __hex_convert(self, integer: int):
        converted = hex(integer).upper()
        while len(converted) < 18:
            converted = "0x0" + converted[2:]

        return converted

    def __set_item(self, cycle_slot: int, item: Item, shuffleslots: list[int]):
        if not isinstance(item, Item):
            raise TypeError(f"{str(type(item))} is not an Item")

        if cycle_slot < 0:
            raise ValueError(f"Cycle slot (Value: {cycle_slot}) cannot be below 0")

        if not item.equippable:
            return

        for item_slot in shuffleslots:
            if not cycle_slot:
                self.__slotmap[item_slot][cycle_slot] = item.id
            else:
                if cycle_slot - 1 in self.__slotmap[item_slot].keys():
                    self.__slotmap[item_slot][cycle_slot] = item.id
                else:
                    raise ValueError(
                        f"The cycle slot (Slot: {cycle_slot-1}) before slot {cycle_slot} doesn't have an Item"
                    )

    def set_item(self, cycle_slot: int, item: Item, side: int = TeamSide.BOTH):
        """
        Sets the item on a specific cycle slot in the config
        """

        if side == TeamSide.BOTH:
            if item.shuffle_slots_t:
                self.set_item(cycle_slot, item, TeamSide.T)
            if item.shuffle_slots_ct:
                self.set_item(cycle_slot, item, TeamSide.CT)

        elif side == TeamSide.T:
            self.__set_item(cycle_slot, item, item.shuffle_slots_t)

        elif side == TeamSide.CT:
            self.__set_item(cycle_slot, item, item.shuffle_slots_ct)

        if item.shuffle_slots:
            self.__set_item(cycle_slot, item, item.shuffle_slots)

    def set_items(self, cycle_slot: int, items: list[Item], side: int = TeamSide.BOTH):
        """
        Sets items starting from the cycle slot in the config
        """
        for item in items:
            self.set_item(cycle_slot, item, side)
            cycle_slot += 1

    def __add_item(
        self, item: Item, shuffleslots: list[int], side: int = TeamSide.BOTH
    ):
        for item_slot in shuffleslots:
            self.set_item(len(self.__slotmap[item_slot]), item, side)

    def add_item(self, item: Item, side: int = TeamSide.BOTH):
        """
        Adds an item on the highest possible cycle slot to the config
        """
        if side == TeamSide.BOTH:
            if item.shuffle_slots_ct:
                self.add_item(item, TeamSide.CT)
            if item.shuffle_slots_t:
                self.add_item(item, TeamSide.T)

        elif side == TeamSide.CT:
            self.__add_item(item, item.shuffle_slots_ct, side)
        elif side == TeamSide.T:
            self.__add_item(item, item.shuffle_slots_t, side)

        if item.shuffle_slots:
            self.__add_item(item, item.shuffle_slots)

    def add_items(self, items, side: int = TeamSide.BOTH):
        """
        Adds a list of items on the highest possible cycle slot to the config
        """
        for item in items:
            self.add_item(item, side)

    def __remove_item(self, item: Item, shuffleslots: list[int]) -> bool:
        if not isinstance(item, Item):
            raise TypeError(f"{str(type(item))} is not an Item")

        removed = False
        for item_slot in shuffleslots:
            for cycle_slot in range(len(self.__slotmap[item_slot])):
                if removed:
                    self.__slotmap[item_slot][cycle_slot - 1] = self.__slotmap[
                        item_slot
                    ][cycle_slot]

                if self.__slotmap[item_slot][cycle_slot] == item.id:
                    del self.__slotmap[item_slot][cycle_slot]
                    removed = True

            if removed and len(self.__slotmap[item_slot]):
                del self.__slotmap[item_slot][len(self.__slotmap[item_slot]) - 1]

        return removed

    def remove_item(self, item: Item, side: int = TeamSide.BOTH) -> bool:
        """
        Removes an item from the config
        """
        ct = t = both = False
        if side == TeamSide.BOTH:

            if item.shuffle_slots_ct:
                ct = self.remove_item(item, TeamSide.CT)
            else:
                ct = True

            if item.shuffle_slots_t:
                t = self.remove_item(item, TeamSide.T)
            else:
                t = True

        elif side == TeamSide.CT:
            ct = t = self.__remove_item(item, item.shuffle_slots_ct)
        elif side == TeamSide.T:
            ct = t = self.__remove_item(item, item.shuffle_slots_t)

        if item.shuffle_slots:
            both = self.__remove_item(item, item.shuffle_slots)
        else:
            both = True

        return ct and t and both

    def remove_items(self, items: list[Item], side: int = TeamSide.BOTH) -> bool:
        """
        Removes a list of items from the config
        """
        success = True
        for item in items:
            if not self.remove_item(item, side):
                success = False

        return success

    def inject_json(self, json: dict) -> None:
        if not isinstance(json, dict):
            raise TypeError("json has to be a dictionary")

        for item_slot in json:
            for n in range(len(json[item_slot])):
                try:
                    item_id = json[item_slot][n]
                except KeyError:
                    if n > 0:
                        raise ValueError(
                            f"Cycle Slot {n} of item slot {item_slot} doesn't have a value"
                        )  # noqa: E501

                self.__slotmap[item_slot][n] = item_id

    def get_dict(self) -> dict:
        return self.__slotmap

    def randomize(self, n: int = 100) -> None:
        """
        Takes the items in the ShuffleConfig
        and stacks them up to a cycle slot n in random order.
        """
        for item_slot in self.__slotmap:
            depending_itemslots = get_depending_item_slots(item_slot)

            items = list()
            for v in self.__slotmap[item_slot].values():
                items.append(v)

            if not items:
                continue

            for i in range(len(items) - 1, n):
                for slot in depending_itemslots:
                    index = int((len(items) - 1) * random())
                    self.__slotmap[slot][i] = items[index]
