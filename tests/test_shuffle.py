from csgoinvshuffle.shuffle import *
from utils import new_shuffleconfig, example_csgo_saved_item_shuffles


def compare_configs():
    assert new_shuffleconfig() == example_csgo_saved_item_shuffles()


def test_shuffle_whole_inventory(inv):
    with ShuffleConfig() as sc:
        sc.add_items(inv)
    compare_configs()
    sc = ShuffleConfig()
    sc.add_items(inv)
    sc.save()
    compare_configs()
