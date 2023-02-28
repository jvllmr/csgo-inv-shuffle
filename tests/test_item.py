from csgoinvshuffle.enums import Rarity
from csgoinvshuffle.item import Item


def test_actual_item(item: Item):
    assert item.stickers[0]["name"] == "Dust II (Gold)"
    assert item.stickers[1]["name"] == "BIG (Gold) | Stockholm 2021"
    assert item.stickers[2]["name"] == "PGL (Gold) | Stockholm 2021"
    assert item.stickers[3]["name"] == "MOUZ (Gold) | Stockholm 2021"

    assert item.id == "1234"
    assert item.custom_name == "1337.reee"
    assert item.equippable
    assert item.rarity == Rarity.RARE
    assert isinstance(repr(item), str)
    assert isinstance(str(item), str)


def test_no_value_item():
    item = Item({}, {}, "")
    for attr_name, attr in item:
        if attr_name == "custom_name":
            assert attr == ""
        elif attr_name == "stickers":
            assert attr == []
        elif attr_name == "equippable":
            assert attr is False
        elif attr_name == "rarity":
            assert attr is None
        elif attr_name == "id":
            assert attr is None
        elif attr_name.startswith("shuffle_slots"):
            assert attr == []
