from utils import example_data
from csgoinvshuffle.inventory import *


def test_parse_inventory():
    inv = parse_inventory(example_data(), "76561198232352624")
    assert isinstance(inv, Inventory)


def test_get_inventory(inv):
    assert inv.owner_id == "76561198232352624"
