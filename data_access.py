# pylint: disable=locally-disabled, too-many-lines, line-too-long
"""
Multiple reference dictionaries are used in the program to match raw strings from the game's code to related data,
either English translations or other information. These are externally made, but as the game's final version has been
released, they are always up-to-date.
"""
import json


def gender_code(gender):
    """
    Accesses dictionary of gender codes.

    :param string gender: The growth rate represented in pokemon.txt.
    :return string: The corresponding gender code.
    """
    with open('references/gender_codes.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(gender)


def growth_rate(rate):
    """
    Accesses dictionary of growth rates.

    :param string rate: The growth rate represented in pokemon.txt.
    :return string: The corresponding growth rate.
    """
    with open('references/growth_rate.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(rate)


def tm_info(number):
    """
    Accesses dictionary of TM info.

    :param string number: The TM number.
    :return string: The corresponding TM info, in the form "canHaveStab,Type".
    """
    with open('references/tm_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(number)


def move_info(move):
    """
    Accesses dictionary of move info.

    :param string move: The move represented in pokemon.txt and tm.txt in title case.
    :return string: The corresponding move info, in the form "MoveName,canHaveSTAB,type".
    """
    with open('references/move_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(move)


def item_info(item):
    """
    Accesses dictionary of item info.

    :param string item: The held item represented in pokemon.txt.
    :return string: The real, English name of the held item.
    """
    with open('references/item_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(item)


def pokemon_info(dex):
    """
    Accesses dictionary of Pokémon info.

    :param string dex: The dex number relating to the Pokémon.
    :return string: The corresponding Pokémon info, as: "INTERNALNAME, displayName".
    """
    with open('references/pokemon_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(dex)


def location_info(zone):
    """
    Accesses dictionary of location info.

    :param string zone: The numbered zone in terms of a string.
    :return string: The English name of the location the zone belongs to.
    """
    with open('references/location_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(zone)


def ability_info(ability):
    """
    Accesses dictionary of ability info.

    :param string ability: The ability name as it appears in pokemon.txt.
    :return string: The English, formatted name of the ability.
    """
    with open('references/ability_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(ability)
