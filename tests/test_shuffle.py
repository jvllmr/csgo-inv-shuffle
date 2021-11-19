from csgoinvshuffle.shuffle import ShuffleConfig
from utils import new_shuffleconfig, example_csgo_saved_item_shuffles


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
