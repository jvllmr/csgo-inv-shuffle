# Description

csgoinvshuffle is a Python package designed to create shuffle configs for the game CS:GO.

With this package you can easily shuffle between different weapon types (e.g. M4A4 and M4A1-S) and have less limits in customizing the shuffle experience than with the in-game settings.

## Note: 
CS:GO never really queues your items in a random order.
The items are arranged in one simple, predefined cycle.
This package aims to creating shuffles to your liking with ease

You can use the config file it creates and replace `<path_to_your_steam>/userdata/<your_steam_3id>/730/remote/cfg/csgo_saved_item_shuffles.txt` with it to apply your config.


#### HINT: 
CS:GO needs to be closed while replacing the file





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

As you can see in the last example, an inventory is equipped with filter attributes and can be handled like a list.
The filters are dynamically generated when you add items to the inventory and you can issue `print(dir(inv))`
to get an overview of the different filter options.
To get an overview of what values the item properties can have, you can lookup https://steamcommunity.com/profiles/YOUR_STEAM_ID_64/inventory/json/730/2.
Typical values for the property `tags_internal_name` are provided by the TagsInternalName enum.


### Create a shuffle cycle for only one team side

```python
from csgoinvshuffle import ShuffleConfig, get_inventory
from csgoinvshuffle.enums import TagsInternalName, TeamSide

with ShuffleConfig() as sc:
    inv = get_inventory("YOUR_STEAM_ID_64")
    knives = inv.filter_by_tags_internal_name(TagsInternalName.KNIVES)
    classic_knife = knives.filter_by_tags_internal_name(TagsInternalName.CLASSIC_KNIFE)[0]
    karambit = knives.filter_by_tags_internal_name(TagsInternalName.KARAMBIT_KNIFE)[0]
    butterfly = knives.filter_by_custom_name("crypto is for n00bs")[0]
    # First map karambit, second map classic knife, third map butterfly, next map karambit again...
    # On T side only
    my_shuffle_cycle = [karambit, classic_knife, butterfly] 
    sc.add_items(my_shuffle_cycle, TeamSide.T)
```

By default, the attribute methods from `ShuffleConfig` do everything for both teams.
If you want to have different shuffle cycles on the opposing sides, you have to state it with a parameter.

