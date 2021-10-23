import subprocess

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


@pytest.fixture(autouse=True)
def inv():
    return inventory
