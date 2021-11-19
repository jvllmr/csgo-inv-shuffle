from functools import cached_property
from csgoinvshuffle.enums import LoadoutSlot, TagsInternalName, TeamSide
from csgoinvshuffle.enums.rarities import Rarity
from csgoinvshuffle.types import (
    Description,
    Action,
    MarketAction,
    SlotTagMap,
    Sticker,
    Tag,
)

from typing import Tuple, Generator, Union

import re

_slot_tag_map_ct: SlotTagMap = {
    LoadoutSlot.AGENT_CT: (TagsInternalName.AGENTS,),
    LoadoutSlot.KNIFE_CT: (TagsInternalName.KNIVES,),
    LoadoutSlot.M4A4: (TagsInternalName.M4A4, TagsInternalName.M4A1_S),
    LoadoutSlot.M4A1_S: (TagsInternalName.M4A4, TagsInternalName.M4A1_S),
    LoadoutSlot.FIVE_SEVEN: (TagsInternalName.FIVE_SEVEN, TagsInternalName.CZ75),
    LoadoutSlot.CZ75_CT: (TagsInternalName.FIVE_SEVEN, TagsInternalName.CZ75),
    LoadoutSlot.USP_S: (TagsInternalName.USP_S, TagsInternalName.P2000),
    LoadoutSlot.P2000: (TagsInternalName.USP_S, TagsInternalName.P2000),
    LoadoutSlot.P250_CT: (TagsInternalName.P250,),
    LoadoutSlot.DEAGLE_CT: (TagsInternalName.DEAGLE, TagsInternalName.REVOLVER),
    LoadoutSlot.REVOLVER_CT: (TagsInternalName.DEAGLE, TagsInternalName.REVOLVER),
    LoadoutSlot.MP9: (TagsInternalName.MP9,),
    LoadoutSlot.MP5_CT: (TagsInternalName.MP5, TagsInternalName.MP7),
    LoadoutSlot.MP7_CT: (TagsInternalName.MP5, TagsInternalName.MP7),
    LoadoutSlot.UMP_45_CT: (TagsInternalName.UMP_45,),
    LoadoutSlot.P90_CT: (TagsInternalName.P90,),
    LoadoutSlot.PP_BIZON_CT: (TagsInternalName.PP_BIZON,),
    LoadoutSlot.FAMAS: (TagsInternalName.FAMAS,),
    LoadoutSlot.AUG: (TagsInternalName.AUG,),
    LoadoutSlot.SSG_08_CT: (TagsInternalName.SSG_08,),
    LoadoutSlot.AWP_CT: (TagsInternalName.AWP,),
    LoadoutSlot.SCAR_20: (TagsInternalName.SCAR_20,),
    LoadoutSlot.NOVA_CT: (TagsInternalName.NOVA,),
    LoadoutSlot.XM1014_CT: (TagsInternalName.XM1014,),
    LoadoutSlot.MAG_7: (TagsInternalName.MAG_7,),
    LoadoutSlot.NEGEV_CT: (TagsInternalName.NEGEV,),
    LoadoutSlot.M249_CT: (TagsInternalName.M249,),
    LoadoutSlot.DUAL_BERETTAS_CT: (TagsInternalName.DUAL_BERETTAS,),
    LoadoutSlot.GLOVES_CT: (TagsInternalName.GLOVES,),
}

_slot_tag_map_t: SlotTagMap = {
    LoadoutSlot.AGENT_T: (TagsInternalName.AGENTS,),
    LoadoutSlot.KNIFE_T: (TagsInternalName.KNIVES,),
    LoadoutSlot.GLOCK_18: (TagsInternalName.GLOCK_18,),
    LoadoutSlot.P250_T: (TagsInternalName.P250,),
    LoadoutSlot.TEC_9: (TagsInternalName.CZ75, TagsInternalName.TEC_9),
    LoadoutSlot.CZ75_T: (TagsInternalName.CZ75, TagsInternalName.TEC_9),
    LoadoutSlot.DEAGLE_T: (TagsInternalName.DEAGLE, TagsInternalName.REVOLVER),
    LoadoutSlot.REVOLVER_T: (TagsInternalName.DEAGLE, TagsInternalName.REVOLVER),
    LoadoutSlot.MAC_10: (TagsInternalName.MAC_10,),
    LoadoutSlot.MP5_T: (TagsInternalName.MP5, TagsInternalName.MP7),
    LoadoutSlot.MP7_T: (TagsInternalName.MP5, TagsInternalName.MP7),
    LoadoutSlot.UMP_45_T: (TagsInternalName.UMP_45,),
    LoadoutSlot.P90_T: (TagsInternalName.P90,),
    LoadoutSlot.PP_BIZON_T: (TagsInternalName.PP_BIZON,),
    LoadoutSlot.GALIL_AR: (TagsInternalName.GALIL_AR,),
    LoadoutSlot.AK_47: (TagsInternalName.AK_47,),
    LoadoutSlot.SG_553: (TagsInternalName.SG553,),
    LoadoutSlot.SSG_08_T: (TagsInternalName.SSG_08,),
    LoadoutSlot.AWP_T: (TagsInternalName.AWP,),
    LoadoutSlot.G3SG1: (TagsInternalName.G3SG1,),
    LoadoutSlot.NOVA_T: (TagsInternalName.NOVA,),
    LoadoutSlot.XM1014_T: (TagsInternalName.XM1014,),
    LoadoutSlot.SAWED_OFF: (TagsInternalName.SAWED_OFF,),
    LoadoutSlot.M249_T: (TagsInternalName.M249,),
    LoadoutSlot.NEGEV_T: (TagsInternalName.NEGEV,),
    LoadoutSlot.DUAL_BERETTAS_T: (TagsInternalName.DUAL_BERETTAS,),
    LoadoutSlot.GLOVES_T: (TagsInternalName.GLOVES,),
}

_slot_tag_map: SlotTagMap = {LoadoutSlot.MUSIC_KIT: (TagsInternalName.MUSIC_KITS,)}

# Market hash names of T agents
_agents_t: tuple[str, ...] = (
    "Sir Bloody Miami Darryl | The Professionals",
    "Sir Bloody Loudmouth Darryl | The Professionals",
    "Sir Bloody Darryl Royale | The Professionals",
    "Sir Bloody Skullhead Darryl | The Professionals",
    "Sir Bloody Silent Darryl | The Professionals",
    "'The Doctor' Romanov | Sabre",
    "The Elite Mr. Muhlik | Elite Crew",
    "Number K | The Professionals",
    "Safecracker Voltzmann | The Professionals",
    "Blackwolf | Sabre",
    "Rezan The Ready | Sabre",
    "Rezan the Redshirt | Sabre",
    "Prof. Shahmat | Elite Crew",
    "Getaway Sally | The Professionals",
    "Little Kev | The Professionals",
    "Osiris | Elite Crew",
    "Slingshot | Phoenix",
    "Dragomir | Sabre",
    "Maximus | Sabre",
    "Street Soldier | Phoenix",
    "Dragomir | Sabre Footsoldier",
    "Enforcer | Phoenix",
    "Ground Rebel | Elite Crew",
    "Soldier | Phoenix",
    "Vypa Sista of the Revolution | Guerrilla Warfare",
    "'Medium Rare' Crasswater | Guerrilla Warfare",
    "Crasswater The Forgotten | Guerrilla Warfare",
    "Elite Trapper Solman | Guerrilla Warfare",
    "Bloody Darryl The Strapped | The Professionals",
    "Arno The Overgrown | Guerrilla Warfare",
    "Col. Mangos Dabisi | Guerrilla Warfare",
    "Trapper | Guerrilla Warfare",
    "Trapper Aggressor | Guerrilla Warfare",
    "Mr. Muhlik | Elite Crew",
)

# Market hash names of CT agents
_agents_ct: tuple[str, ...] = (
    "Special Agent Ava | FBI",
    "Lt. Commander Ricksaw | NSWC SEAL",
    "Cmdr. Mae 'Dead Cold' Jamison | SWAT",
    "1st Lieutenant Farlow | SWAT",
    "'Two Times' McCoy | USAF TACP",
    "Michael Syfers | FBI Sniper",
    "'Two Times' McCoy | TACP Cavalry",
    "John 'Van Healen' Kask | SWAT",
    "Sergeant Bombson | SWAT",
    "'Blueberries' Buckshot | NSWC SEAL",
    "Buckshot | NSWC SEAL",
    "Markus Delrow | FBI HRT",
    "Chem-Haz Specialist | SWAT",
    "3rd Commando Company | KSK",
    "Seal Team 6 Soldier | NSWC SEAL",
    "Bio-Haz Specialist | SWAT",
    "B Squadron Officer | SAS",
    "Operator | FBI SWAT",
    "Chef d'Escadron Rouchard | Gendarmerie Nationale",
    "Cmdr. Frank 'Wet Sox' Baroud | SEAL Frogman",
    "Cmdr. Davida 'Goggles' Fernandez | SEAL Frogman",
    "Chem-Haz Capitaine | Gendarmerie Nationale",
    "Lieutenant Rex Krikey | SEAL Frogman",
    "Officer Jacques Beltram | Gendarmerie Nationale",
    "Lieutenant 'Tree Hugger' Farlow | SWAT",
    "Sous-Lieutenant Medic | Gendarmerie Nationale",
    "Primeiro Tenente | Brazilian 1st Battalion",
    "D Squadron Officer | NZSAS",
    "Aspirant | Gendarmerie Nationale",
)

_equippable: tuple = (
    "weapon_",
    TagsInternalName.GLOVES,
    TagsInternalName.KNIVES,
    TagsInternalName.MUSIC_KITS,
    TagsInternalName.AGENTS,
)


class Item:
    """Represents a CS:GO Item"""

    assetid: str
    classid: str
    instanceid: str
    contextid: str
    amount: str
    pos: int
    appid: str
    icon_url: str
    icon_url_large: str
    icon_drag_url: str
    name: str
    market_hash_name: str
    market_name: str
    name_color: str
    background_color: str
    type: str
    tradable: int
    marketable: int
    commodity: int
    market_tradable_restriction: str
    descriptions: list[Description]
    owner_descriptions: str
    actions: list[Action]
    market_actions: list[MarketAction]
    tags: list[Tag]
    fraudwarnings: list[str]

    def __init__(self, description, asset, steamid64):
        for k, v in asset.items():
            setattr(self, k, v)
        for k, v in description.items():
            if k == "actions" or k == "market_actions":
                for action in range(len(v)):
                    v[action]["link"] = (
                        v[action]["link"]
                        .replace(r"%assetid%", str(self.id))
                        .replace(r"%20M%listingid%", f" S{steamid64}")
                    )
            setattr(self, k, v)

    def __iter__(self) -> Generator[Tuple[str, Union[str, int]], None, None]:
        for attr in dir(self):
            if not attr.startswith("_"):
                yield attr, getattr(self, attr)

    def __repr__(self):
        return str(dict(self))

    def __str__(self):
        custom_name_string = ""
        if self.custom_name:
            custom_name_string = f"custom_name: '{self.custom_name}', "
        return f"<Item name: '{self.name}' {custom_name_string} id: {self.id}>"

    @cached_property
    def id(self) -> str:
        return self.assetid

    @cached_property
    def custom_name(self) -> str:
        if attr := getattr(self, "fraudwarnings", ""):
            return attr[0].split(":", 1)[1].lstrip(" ").strip("'")
        else:
            return ""

    @cached_property
    def stickers(self) -> list[Sticker]:
        for desc in self.descriptions:
            if "sticker_info" in (val := desc.get("value", "")):
                stickers: list[Sticker] = list()
                regex_name = "Sticker" if "Sticker" in val else "Patch"
                regex_link = "stickers" if "Sticker" in val else "patches"

                links = iter(
                    re.findall(
                        rf"https://steamcdn-a\.akamaihd\.net/apps/730/icons/econ/{regex_link}[\w|\d|\.|\/]+\.png",  # noqa: E501
                        val,
                    )
                )

                names = iter(
                    re.findall(rf"<br>{regex_name}:[\w|\s|\(|\)|\,]+", val)[0]
                    .lstrip("<br>Patch: ")
                    .split(", ")
                )

                try:
                    while True:
                        stickers.append({"link": next(links), "name": next(names)})
                except StopIteration:
                    return stickers
        return []

    @cached_property
    def rarity(self) -> Union[str, None]:
        for tag in self.tags:
            if tag["category"] == "Rarity":
                for rarity in Rarity:
                    if rarity.value.lower() in tag["internal_name"].lower():
                        return rarity.value
        return None

    @cached_property
    def equippable(self) -> bool:
        for tag in self.tags:
            for name in _equippable:
                if name in tag["internal_name"]:
                    return True
        return False

    def __shuffle_slots(self, side=None) -> list[int]:
        if side == TeamSide.CT:
            needed_map = _slot_tag_map_ct
        elif side == TeamSide.T:
            needed_map = _slot_tag_map_t
        else:
            needed_map = _slot_tag_map

        slots = list()

        for slot, tag_names in needed_map.items():
            for tag in self.tags:
                if (internal_name := tag["internal_name"]) in tag_names:
                    if internal_name == TagsInternalName.AGENTS:
                        if side == TeamSide.CT and self.market_hash_name in _agents_ct:
                            slots.append(slot.value)
                        elif side == TeamSide.T and self.market_hash_name in _agents_t:
                            slots.append(slot.value)
                    else:
                        slots.append(slot.value)

        return slots if self.equippable else []

    @cached_property
    def shuffle_slots_t(self) -> list[int]:
        return self.__shuffle_slots(TeamSide.T)

    @cached_property
    def shuffle_slots_ct(self) -> list[int]:
        return self.__shuffle_slots(TeamSide.CT)

    @cached_property
    def shuffle_slots(self) -> list[int]:
        return self.__shuffle_slots()
