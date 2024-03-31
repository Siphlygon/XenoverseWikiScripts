# pylint: disable=locally-disabled, too-many-lines, line-too-long
"""
Multiple JSON reference dictionaries are used in the program to match raw strings from the game's code to related data,
either English translations or other information. These are externally made, but as the game's final version has been
released, they are always up-to-date, not counting human error (my own). The dictionaries are loaded in the functions
below, and are used in the main program to generate the wiki page.
"""
import json


def gender_code(gender):
    """
    Accesses dictionary of gender codes.

    Pokémon have different rates of being either male or female. Pokémon may also be genderless, which is guaranteed if
    applicable. This dictionary is used to convert the game's internal representation of a gender code into a number
    representing the same for the wiki's display.

    Format: "GenderRate" -> "GenderCode"

    :param string gender: The growth rate represented in pokemon.txt.
    :return string: The corresponding gender code.
    """
    with open('references/gender_codes.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(gender)


def growth_rate(rate):
    """
    Accesses a dictionary of growth rates.

    Pokémon are grouped into experience groups, which determine how much EXP they need to level up. This dictionary is
    used to convert the game's internal representation of growth rates to a number, which the wiki uses to display the
    growth rate in another format.

    Format: "GrowthRate" -> "EXPNumber"

    :param string rate: The growth rate as represented in pokemon.txt.
    :return string: The corresponding number representing the related experience group.
    """
    with open('references/growth_rate.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(rate)


def tm_info(move):
    """
    Accesses a dictionary of TM info.

    TMs are stored as move names in tm.txt, but are converted to TM numbers (01-95) for the wiki, which is what the
    reference dictionary is used for. The type of each TM and if the move can gain STAB are also stored in this
    dictionary.

    Format: "TMName" -> {"TMNo": "TMNo", "STAB": "yes/no", "Type": "Type"}

    :param string move: The move represented in pokemon.txt and tm.txt in title case.
    :return string: A dictionary for the TMNo, STAB, and type.
    """
    with open('references/tm_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(move)


def move_info(move):
    """
    Accesses a dictionary of move info.

    Every move in the wiki's move templates is stored in this dictionary, along with its proper name, if it can gain
    STAB, and its type. This is used to format moves in the wiki page.

    Format: "MoveName" -> {"Name": "MoveName", "STAB": "yes/no", "Type": "Type"}

    :param string move: The move represented in pokemon.txt and tm.txt in title case.
    :return string: A dictionary for the move name, STAB, and type.
    """
    with open('references/move_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(move)


def wild_item_info(item):
    """
    Accesses a dictionary of wild item info.

    This does not account for every item in the game, just any item that can appear as a wild held item. This is often
    stored in Italian or otherwise without spaces in the game's data, so this dictionary is used to convert the game's
    internal representation to the English name.

    Format: "ItemInternalName" -> "ItemDisplayName"

    :param string item: The held item represented in pokemon.txt.
    :return string: The real, English name of the held item.
    """
    with open('references/wild_item_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(item)


def pokemon_info(dex):
    """
    Accesses a dictionary of Pokémon info.

    This is used to convert a dex number to its respective Pokémon name, which is used in the wiki page. Dex number was
    chosen as the next and previous Pokémon are determined by adjusting this number. This retrieves both the internal
    name and the display name of the Pokémon.

    Format: "DexNumber" -> {"InternalName": "InternalName", "DisplayName": "DisplayName"}

    :param string dex: The dex number relating to the Pokémon.
    :return string: A dictionary for the internal name and display name.
    """
    with open('references/pokemon_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(dex)


def location_info(zone):
    """
    Accesses a dictionary of location info.

    Locations consist of multiple numbered zones in the game, and this dictionary matches said zones to English location
    names, which were manually translated both through software and by cross-referencing the English wiki and the
    Italian wiki.

    Format: "ZoneNumber" -> "LocationRealName"

    :param string zone: The numbered zone in terms of a string.
    :return string: The English name of the location the zone belongs to.
    """
    with open('references/location_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(zone)


def ability_info(ability):
    """
    Accesses a dictionary of ability info.

    Abilities are stored as fully capitalised names in the game data, and they often require spaces inputted for display
    purposes. This dictionary is used for that exact purpose, and contains every ability a Pokémon can have in
    Xenoverse.

    Format: "AbilityInternalName" -> "AbilityDisplayName"

    :param string ability: The ability name as it appears in pokemon.txt.
    :return string: The English, formatted name of the ability.
    """
    with open('references/ability_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(ability)


def ability_immunities(ability):
    """
    Accesses a dictionary of ability immunities.

    This dictionary contains all abilities that grant immunities to certain types of moves, regardless of secondary
    effects. This is used to indicate which abilities do so for the purpose of calculating type effectiveness.

    Format: "AbilityInternalName" -> "ImmunityType"

    :param string ability: The ability name as it appears in pokemon.txt.
    :return string: The immunity gained by the Pokémon.
    """
    with open('references/ability_immunities.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(ability)


def static_encounters(pokemon):
    """
    Accesses a dictionary of static encounters.

    Said dictionary has unreachable elements (namely, Alolan forms) for the purpose of record, and possible future
    implementation. This dictionary is used to determine the type of static encounter a Pokémon has, which can be either
    a gift, a trade, or a battle. This is always displayed for any applicable Pokémon.

    Format: "PokemonInternalName" -> {"LocationName": "EncounterType"}

    :param string pokemon: The pokemon's internal name as it appears in pokemon.txt.
    :return dict[str, str]: A dictionary with location names as a key and the type of static encounter as a value.
    """
    with open('references/static_encounters.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(pokemon)


def species_and_dex_entry(internal_num):
    """
    Accesses a dictionary of species names and entry numbers.

    The English species name and dex entry are stored in a massive english.txt file. They are related to a Pokémon by
    an internal number, which is a widely varying metric that unimplemented Pokémon also have. This dictionary is used
    to convert the internal number of implemented Pokémon to the species name and dex entry.

    Format: "PokemonInternalNumber" -> {"Species": "SpeciesName", "Dex Entry": "DexEntry"}

    :param string internal_num: The pokemon's internal number as it appears in pokemon.txt.
    :return dict[str, str]: A dictionary for the species name and dex entry.
    """
    with open('references/species_and_dex_entry.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(internal_num)


def location_order():
    """
    Accesses a dictionary of location names and index numbers.

    An artificial order is created to order the locations displayed in the availability information, as the encounter
    information has a random order. Every location has an order in this dictionary, and the whole dictionary is used to
    sort the locations in the wiki page.

    Format: {"LocationName": LocationIndex}

    :return dict[str, int]: A dictionary of locations and associated indexes.
    """
    with open('references/location_order.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch


def evolution_info(internal_name):
    """
    Accesses a dictionary of evolution info.

    Pre-evolution information is not stored with a Pokémon in the game data, and you would need to search the entire
    file otherwise. This dictionary is instead used as a convenience to establish the evolutionary chain of a Pokémon
    line. Pre-evolution method is stored because it's a one-to-one relationship (every evo has exactly 1 pre-evo)
    compared to e.g., gloom having 2 evos.

    Format: "PokémonInternalName" -> {"PreEvolution": "PreEvolution", "Evolution": ["Evolution"], "PreEvoMethod": {"Method": "Info"}}

    :return dict[str, str | list[str] | dict[str, str]]: A dictionary of pre-evo, evo, and pre-evo method information.
    """
    with open('references/evolution_info.json', encoding="utf-8") as f:
        switch = json.load(f)
    return switch.get(internal_name)
