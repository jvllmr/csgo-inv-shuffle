from subprocess import run
try:
    from csgoinvshuffle import get_inventory
except ModuleNotFoundError:
    raise ModuleNotFoundError('Please run "pip install ." in the projects root directory')
import pytest


def test_install():
    assert run(['pip', 'install', '-r', "requirements.txt"]).returncode == 0
    assert run(['pip', 'install', '.', '--use-feature=in-tree-build']).returncode == 0


inventory = get_inventory("76561198232352624")


@pytest.fixture(autouse=True)
def inv():
    return inventory


test_install()
