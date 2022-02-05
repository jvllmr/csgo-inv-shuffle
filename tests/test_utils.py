import pytest

from csgoinvshuffle.enums import LoadoutSlot
from csgoinvshuffle.item import _slot_tag_map, _slot_tag_map_ct, _slot_tag_map_t
from csgoinvshuffle.types import SlotTagMap
from csgoinvshuffle.utils import get_depending_item_slots, get_loadout_slot_enum_value


def test_get_loadout_slot_enum_value():
    for enum_value in LoadoutSlot:
        assert get_loadout_slot_enum_value(enum_value.value) == enum_value

    with pytest.raises(ValueError):
        get_loadout_slot_enum_value(1)


def __test_get_depending_item_slots(slot_tag_map: SlotTagMap):
    for enum_value, tuple_ in slot_tag_map.items():
        assert_ = len(get_depending_item_slots(enum_value.value))
        if enum_value != LoadoutSlot.AGENT_CT and enum_value != LoadoutSlot.AGENT_T:
            assert assert_ == len(tuple_)
        else:
            assert assert_ == 1


def test_get_depending_item_slots():
    __test_get_depending_item_slots(_slot_tag_map)


def test_get_depending_item_slots_t():
    __test_get_depending_item_slots(_slot_tag_map_t)


def test_get_depending_item_slots_ct():
    __test_get_depending_item_slots(_slot_tag_map_ct)
