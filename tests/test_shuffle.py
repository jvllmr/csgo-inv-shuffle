from copy import deepcopy

import pytest
from utils import example_csgo_saved_item_shuffles, new_shuffleconfig

from csgoinvshuffle.enums import LoadoutSlot, TeamSide
from csgoinvshuffle.item import Item
from csgoinvshuffle.shuffle import ShuffleConfig, SlotMap


def compare_configs():
    assert example_csgo_saved_item_shuffles() == new_shuffleconfig()


def test_shuffle_whole_inventory(inv):
    sc = ShuffleConfig()
    sc.add_items(inv)
    sc.save()
    compare_configs()


def test_shuffle_whole_inventory_with(inv):
    with ShuffleConfig() as sc:
        sc.add_items(inv)
    compare_configs()


def test_slotmap(item: Item):
    assert SlotMap([]) == [(enum.value, []) for enum in LoadoutSlot]
    slotmap = SlotMap(
        [(LoadoutSlot.AK_47.value, ["1234"]), (LoadoutSlot.REVOLVER_CT.value, ["543"])]
    )
    assert (LoadoutSlot.AK_47.value, ["1234"]) in slotmap
    assert (LoadoutSlot.DEAGLE_CT.value, ["543"]) in slotmap
    assert (LoadoutSlot.DEAGLE_T.value, ["543"]) not in slotmap
    assert (LoadoutSlot.M4A1_S.value, []) in slotmap
    with pytest.raises(ValueError):
        SlotMap([("12345", [])])

    with pytest.raises(TypeError):
        SlotMap([(LoadoutSlot.AK_47, [1234])])

    slotmap[LoadoutSlot.AK_47] = "abc"
    assert slotmap[LoadoutSlot.AK_47] == (LoadoutSlot.AK_47, ["abc"])
    slotmap[LoadoutSlot.AK_47] = ["abc", "1234"]
    slotmap.append(LoadoutSlot.AGENT_CT, "AAAAA")
    assert slotmap[LoadoutSlot.AGENT_CT][1][-1] == "AAAAA"

    slotmap.remove(LoadoutSlot.AK_47, item)
    assert slotmap[LoadoutSlot.AK_47][1] == ["abc"]

    slotmap[LoadoutSlot.MAC_10] = ["wow", "this", "is", "a", "test"]
    slotmap.insert(LoadoutSlot.MAC_10, 2, item)
    assert slotmap[LoadoutSlot.MAC_10] == (
        LoadoutSlot.MAC_10,
        ["wow", "this", item.id, "is", "a", "test"],
    )


def test_randomize(inv):
    sc = ShuffleConfig()
    sc.add_items(inv)
    sc.randomize()
    for _, id_list in sc._slotmap:
        assert len(id_list) == 100


def test_operations(item: Item):

    item2 = deepcopy(item)
    item3 = deepcopy(item)
    item2.assetid = "5678"
    item3.assetid = "abc"

    for side in TeamSide:
        sc = ShuffleConfig()
        sc.set_items(0, [item, item2, item3], side)
        assert (
            sc._slotmap[LoadoutSlot.UMP_45_CT][1]
            == [
                item.id,
                item2.id,
                item3.id,
            ]
            or sc._slotmap[LoadoutSlot.UMP_45_T][1] == [item.id, item2.id, item3.id]
        )

        sc.insert_items([item3, item], 2, side)

        assert sc._slotmap[LoadoutSlot.UMP_45_CT][1] == [
            item.id,
            item2.id,
            item3.id,
            item.id,
            item3.id,
        ] or sc._slotmap[LoadoutSlot.UMP_45_T][1] == [
            item.id,
            item2.id,
            item3.id,
            item.id,
            item3.id,
        ]

        assert sc.remove_items([item2, item3], side) is True
        assert (
            sc._slotmap[LoadoutSlot.UMP_45_CT][1]
            == [
                item.id,
                item.id,
                item3.id,
            ]
            or sc._slotmap[LoadoutSlot.UMP_45_T][1] == [item.id, item.id, item3.id]
        )
