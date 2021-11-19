from csgoinvshuffle.enums import LoadoutSlot
from typing import List
from csgoinvshuffle.item import _slot_tag_map, _slot_tag_map_ct, _slot_tag_map_t
from csgoinvshuffle.types import SlotTagMap


def get_loadout_slot_enum_value(item_slot: int) -> LoadoutSlot:
    for enum in LoadoutSlot:
        if enum == item_slot:
            return enum
    raise ValueError(f"Item Slot {item_slot} does not exist")


def __get_depending_item_slots(
    loadout_slot: LoadoutSlot, slot_tag_map: SlotTagMap
) -> List[int]:
    def compare(x, y):
        for e in x:
            if e not in y:
                return False
        return True

    depending_item_slots = list()
    compare_value = slot_tag_map[loadout_slot]
    for k, v in slot_tag_map.items():
        if compare(v, compare_value):
            depending_item_slots.append(k.value)

    while loadout_slot.value in depending_item_slots:
        depending_item_slots.remove(loadout_slot.value)
    depending_item_slots.append(loadout_slot.value)

    return depending_item_slots


def get_depending_item_slots(item_slot: int) -> List[int]:
    enum_value = get_loadout_slot_enum_value(item_slot)
    if enum_value in _slot_tag_map_t.keys():
        return __get_depending_item_slots(enum_value, _slot_tag_map_t)
    elif enum_value in _slot_tag_map_ct.keys():
        return __get_depending_item_slots(enum_value, _slot_tag_map_ct)
    else:
        return __get_depending_item_slots(enum_value, _slot_tag_map)
