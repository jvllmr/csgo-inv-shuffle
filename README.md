# Description

csgoinvshuffle is a Python package designed to create shuffle configs for the game CS:GO.

With this package you can easily shuffle between different weapon types (e.g. M4A4 and M4A1-S) and have less limits in cusomizing the shuffle experience than in the in-game settings.

##Note: 
CS:GO never really queues your items in a random order.
The items are arranged in one simple cycle.

You can use the config file it creates and replace `<path_to_your_steam>/userdata/<your_steam_3id>/730/remote/cfg/csgo_saved_item_shuffles.txt` with it to apply your config.


###HINT: CS:GO needs to be closed while replacing the file





# How to install

The package requires Python 3.9:
```pip install csgoinvshuffle```

# Basic usage

## Your steam inventory needs to be public!
### Basic shuffle for everything in your inventory

```python
from csgoinvshuffle import ShuffleConfig, get_inventory

with ShuffleConfig() as sc:
    sc.add_items(get_inventory("YOUR_STEAM_ID_64"))

```

### Give items a certain order in the cycle
```python
from csgoinvshuffle import ShuffleConfig, get_inventory
from csgoinvshuffle.enums import TagsInternalName

# This example only works if you have at least 4 music kits in your inventory
sc = ShuffleConfig()
inv = get_inventory("YOUR_STEAM_ID_64")
music_kits = inv.filter_by_tags_internal_name(TagsInternalName.MUSIC_KITS)
sc.set_item(0 , music_kits[3])
sc.set_item(1, music_kits[1])
sc.save()
```

