from __future__ import annotations

from csgoinvshuffle.utils import get_depending_item_slots, get_loadout_slot_enum_value
from csgoinvshuffle.item import Item
from csgoinvshuffle import shuffleformat
from csgoinvshuffle.enums import LoadoutSlot, TeamSide
from functools import cache, reduce
from os.path import abspath
from random import random
import typing as t


class SlotMap(list):
    def __init__(self, lst: list[t.Tuple[int, list[str]]] = None):
        if lst:

            for loadout_slot, item_ids in lst:
                try:
                    get_loadout_slot_enum_value(loadout_slot)
                except ValueError:
                    raise ValueError(f"{loadout_slot} is not a valid loadoutslot")
                for id in item_ids:
                    if not isinstance(id, str):
                        raise TypeError(f"{item_ids} must be a list of strings")

                # Adjust depending loadout slots
                for other_slot in get_depending_item_slots(loadout_slot):
                    if other_slot not in map(lambda x: x[0], lst):
                        lst.append((other_slot, item_ids))
                    else:
                        for other_loadout_slot, other_item_ids in lst:
                            if other_slot == other_loadout_slot:
                                assert item_ids == other_item_ids
                                break
            # Add the missing loadout slots
            for enum in LoadoutSlot:
                if enum.value not in map(lambda x: x[0], lst):
                    lst.append((enum.value, []))
        else:
            lst = list()
            for enum in LoadoutSlot:
                lst.append((enum.value, []))
        super().__init__(lst)

    def __iter__(self) -> t.Generator[t.Tuple[int, list[str]], None, None]:
        yield from super().__iter__()

    def __getitem__(self, index: int):  # type: ignore
        for _tuple in self:
            if _tuple[0] == index:
                return _tuple

    def __setitem__(self, index: int, value: t.Union[list[str], str]):  # type: ignore
        if isinstance(value, str):
            value = [value]
        for _index, _tuple in enumerate(self):
            if _tuple[0] == index:
                return super().__setitem__(_index, (_tuple[0], value))

    def append(  # type:ignore
        self, item_slot: t.Union[int, LoadoutSlot], item: t.Union[Item, str]
    ):
        if isinstance(item, Item):
            item = item.id
        if isinstance(item_slot, LoadoutSlot):
            item_slot = item_slot.value
        self[item_slot][1].append(item)

    def remove(  # type: ignore
        self, item_slot: t.Union[int, LoadoutSlot], item: t.Union[Item, str]
    ) -> bool:
        if isinstance(item, Item):
            item = item.id
        if isinstance(item_slot, LoadoutSlot):
            item_slot = item_slot.value
        return self[item_slot][1].remove(item)

    def insert(  # type: ignore
        self,
        item_slot: t.Union[int, LoadoutSlot],
        cycle_slot: int,
        item: t.Union[Item, str],
    ):
        if isinstance(item, Item):
            item = item.id
        if isinstance(item_slot, LoadoutSlot):
            item_slot = item_slot.value
        self[item_slot][1].insert(cycle_slot, item)


class ShuffleConfig:
    def __init__(self, path: str = "./csgo_saved_item_shuffles.txt"):
        self.path = abspath(path)
        self._slotmap = SlotMap()

    def __exit__(self, exc_type, *_):
        if not exc_type:
            self.save()

    def __enter__(self) -> ShuffleConfig:
        return self

    def generate(self) -> str:
        """
        Returns the config content as a string
        """
        ret = shuffleformat.HEADER
        for item_slot, item_ids in self._slotmap:
            items = str()
            for cycle_slot, item_id in enumerate(item_ids):

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
    def __hex_convert(self, integer: int) -> str:
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
            self._slotmap[item_slot] = item.id

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
        if not isinstance(item, Item):
            raise TypeError(f"{str(type(item))} is not an Item")
        for item_slot in shuffleslots:
            self._slotmap.append(item_slot, item)

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
        lst: list[bool] = list()
        for item_slot in shuffleslots:
            lst.append(self._slotmap.remove(item_slot, item))

        return reduce(lambda x, y: x and y, lst)

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

    def __insert_item(self, item: Item, cycle_slot: int, shuffleslots: list[int]):
        if not isinstance(item, Item):
            raise TypeError(f"{str(type(item))} is not an Item")
        for item_slot in shuffleslots:
            self._slotmap.insert(item_slot, cycle_slot, item)

    def insert_item(self, item: Item, cycle_slot: int, side: int = TeamSide.BOTH):
        """
        Inserts an Item into the config on a cycle slot
        """
        if side == TeamSide.BOTH:
            self.__insert_item(item, cycle_slot, item.shuffle_slots_ct)
            self.__insert_item(item, cycle_slot, item.shuffle_slots_t)
        elif side == TeamSide.CT:
            self.__insert_item(item, cycle_slot, item.shuffle_slots_ct)
        elif side == TeamSide.T:
            self.__insert_item(item, cycle_slot, item.shuffle_slots_t)

        if item.shuffle_slots:
            self.__insert_item(item, cycle_slot, item.shuffle_slots)

    def insert_items(
        self, items: list[Item], cycle_slot: int, side: int = TeamSide.BOTH
    ):
        """
        Inserts an Items into the config on a cycle slot
        """
        for item in items:
            self.insert_item(item, cycle_slot, side)
            cycle_slot += 1

    def randomize(self, n: int = 100) -> None:
        """
        Takes the items in the ShuffleConfig
        and stacks them up to a cycle slot n in random order.
        """
        for item_slot, item_ids in self._slotmap:
            depending_itemslots = get_depending_item_slots(item_slot)

            if not item_ids:
                continue

            for _ in range(len(item_ids) - 1, n):
                for slot in depending_itemslots:
                    index = int((len(item_ids) - 1) * random())
                    self._slotmap.append(slot, item_ids[index])
