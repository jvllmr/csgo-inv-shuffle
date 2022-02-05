from enum import IntEnum, auto

import pytest

from csgoinvshuffle.enums import TagsInternalName
from csgoinvshuffle.inventory import Inventory, NotAnItemError, get_inventory
from csgoinvshuffle.item import Item


def test_parse_inventory(inv: Inventory):
    assert isinstance(inv, Inventory)
    # assert repr(inv) == example_inv_repr()


def test_get_inventory(inv: Inventory):
    test_inv = get_inventory("76561198232352624")
    assert test_inv.owner_id == inv.owner_id
    for i in range(len(test_inv)):
        assert isinstance(test_inv[i], Item)
    assert get_inventory("") is None

    with pytest.raises(NotAnItemError):
        test_inv.append(1)

    assert isinstance(repr(test_inv), str)
    assert isinstance(str(test_inv), str)


def test_filter(inv: Inventory):

    filtered = list(
        filter(
            lambda x: x.custom_name == "Irgendwie...NICHT",
            inv.filter(TagsInternalName.DEAGLE),
        )
    )

    assert len(filtered) == 1

    class RandomEnum(IntEnum):
        WOW = auto()

    with pytest.raises(ValueError):
        inv.filter(RandomEnum.WOW, RandomEnum)

    with pytest.raises(TypeError):
        inv.filter(RandomEnum.WOW, "ABC")
