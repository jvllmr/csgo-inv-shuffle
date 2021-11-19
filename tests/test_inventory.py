from csgoinvshuffle.inventory import get_inventory, Inventory


def test_parse_inventory(inv: Inventory):
    assert isinstance(inv, Inventory)
    # assert repr(inv) == example_inv_repr()


def test_get_inventory(inv: Inventory):
    assert get_inventory("76561198232352624").owner_id == inv.owner_id
