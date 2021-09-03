
from subprocess import run
try:
    from csgoinvshuffle.inventory import parse_inventory
except ModuleNotFoundError:
    raise ModuleNotFoundError('Please run "pip install ." in the projects root directory')
import pytest
import utils


def test_install():
    assert run(['pip', 'install', '-r', "requirements.txt"]).returncode == 0
    assert run(['pip', 'install', '.', '--use-feature=in-tree-build']).returncode == 0


inventory = parse_inventory(utils.example_data(), "76561198232352624")


@pytest.fixture(autouse=True)
def inv():
    return inventory


test_install()
