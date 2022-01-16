from csgoinvshuffle.shuffle import ShuffleConfig, SlotMap
from utils import new_shuffleconfig, example_csgo_saved_item_shuffles
from csgoinvshuffle.enums import LoadoutSlot


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


def test_create_slotmap():
    assert SlotMap([]) == [(enum.value, []) for enum in LoadoutSlot]
    slotmap = SlotMap(
        [(LoadoutSlot.AK_47.value, ["1234"]), (LoadoutSlot.REVOLVER_CT.value, ["543"])]
    )
    assert (LoadoutSlot.AK_47.value, ["1234"]) in slotmap
    assert (LoadoutSlot.DEAGLE_CT.value, ["543"]) in slotmap
    assert (LoadoutSlot.M4A1_S.value, []) in slotmap
