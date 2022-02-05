import subprocess

from csgoinvshuffle.item import Item

try:
    from csgoinvshuffle.inventory import parse_inventory
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        'Please run "python -m poetry install" in the projects root directory'
    )
import pytest
import utils

subprocess.run(["poetry", "install"])

inventory = parse_inventory(utils.example_data(), "76561198232352624")


@pytest.fixture(scope="session")
def inv():
    return inventory


@pytest.fixture(scope="session")
def item():
    return Item(
        {},
        {
            "name": "test_item",
            "assetid": "1234",
            "tags": [
                {
                    "category": "Type",
                    "internal_name": "CSGO_Type_SMG",
                    "localized_category_name": "Type",
                    "localized_tag_name": "SMG",
                },
                {
                    "category": "Weapon",
                    "internal_name": "weapon_ump45",
                    "localized_category_name": "Weapon",
                    "localized_tag_name": "UMP-45",
                },
                {
                    "category": "ItemSet",
                    "internal_name": "set_stmarc",
                    "localized_category_name": "Collection",
                    "localized_tag_name": "The St. Marc Collection",
                },
                {
                    "category": "Quality",
                    "internal_name": "normal",
                    "localized_category_name": "Category",
                    "localized_tag_name": "Normal",
                },
                {
                    "category": "Rarity",
                    "internal_name": "Rarity_Rare_Weapon",
                    "localized_category_name": "Quality",
                    "localized_tag_name": "Mil-Spec Grade",
                    "color": "4b69ff",
                },
                {
                    "category": "Exterior",
                    "internal_name": "WearCategory2",
                    "localized_category_name": "Exterior",
                    "localized_tag_name": "Field-Tested",
                },
            ],
            "fraudwarnings": ["Name Tag: ''1337.reee''"],
            "descriptions": [
                {
                    "type": "html",
                    "value": """
                    <br>
                    <div id="sticker_info" name="sticker_info" title="Sticker" style="border: 2px solid rgb(102, 102, 102); border-radius: 6px; width=100; margin:4px; padding:8px;">
                    <center>
                    <img width=64 height=48 src="https://steamcdn-a.akamaihd.net/apps/730/icons/econ/stickers/tournament_assets/de_dust2_gold.d203a911e55d6429d53ba5652e8088d7c9a5b151.png">
                    <img width=64 height=48 src="https://steamcdn-a.akamaihd.net/apps/730/icons/econ/stickers/stockh2021/big_gold.ce45768a7730fee03e56c39eba0a89f9f23599ec.png">
                    <img width=64 height=48 src="https://steamcdn-a.akamaihd.net/apps/730/icons/econ/stickers/stockh2021/pgl_gold.e78a028f9fe095047c344e3e0718ec8ecf75137b.png">
                    <img width=64 height=48 src="https://steamcdn-a.akamaihd.net/apps/730/icons/econ/stickers/stockh2021/mouz_gold.5bca1473fe7da7964f00cd6b1d0d902aec0b19f1.png">
                    <br>Sticker: Dust II (Gold), BIG (Gold) | Stockholm 2021, PGL (Gold) | Stockholm 2021, MOUZ (Gold) | Stockholm 2021
                    </center>
                    </div>""",
                }
            ],
        },
        "",
    )
