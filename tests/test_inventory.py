from utils import example_data, example_inv_repr
from csgoinvshuffle.inventory import *


def test_parse_inventory(inv: Inventory):
    assert isinstance(inv, Inventory)
    #assert repr(inv) == example_inv_repr()


def test_get_inventory(inv: Inventory):
    assert get_inventory("76561198232352624").owner_id == inv.owner_id
