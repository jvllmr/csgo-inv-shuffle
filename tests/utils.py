import json


def __read_file(file: str):
    f = open("tests/test_data/" + file, "r", encoding="utf-8")
    data = f.read()
    f.close()
    return data


def example_data() -> dict:
    d = __read_file("test_inventory.json")
    return json.loads(d)


def example_csgo_saved_item_shuffles() -> str:
    return __read_file("compare_data.txt")


def example_inv_repr() -> str:
    return __read_file("inventory_repr.txt")


def new_shuffleconfig() -> str:
    f = open("./csgo_saved_item_shuffles.txt", "r", encoding="utf-8")
    data = f.read()
    f.close()
    return data
