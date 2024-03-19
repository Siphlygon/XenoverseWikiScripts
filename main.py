# -*- coding: utf-8 -*-
# pylint: disable=locally-disabled, too-many-lines, line-too-long
"""
Create Pokémon page script for the Pokémon Xenoverse Wiki.

Reads in a given internal name matching a Pokémon in the game data for Pokémon Xenoverse. Contains a copy of the
relevant game files for use and access, and a set of custom reference dictionaries matching strings in the game data to
associated information.

Prints lines in the style of the Pokémon Xenoverse Wiki code. These can be copied and pasted straight onto the wiki page
and will render correctly.

NOTE: VintageDex functionality is not complete, not a priority until all important information for main dex & XenoDex
are complete.
I have chosen not to add multiple form functionality, both due to its sparcity and the difficulty of retrieving related
information (they are not in the standard text files).

Elements still to implement:
- species (may not be possible in English)
- availability
  * static encounters
  * breeding & evolution
- egg move fathers
- evolution
  * in the evolution box at the end of the page
  * in indicating future STAB in the move learn lists
  * in the opening paragraph box
- pokédex entries (may not be possible in English)

@author: Siphlygon
Last Updated: 18th March 2024
"""

import json
import logging
import traceback


# region Reference Dictionaries
def gender_code(gender):
    """
    Accesses dictionary of gender codes.

    :param string gender: The growth rate represented in pokemon.txt.
    :return string: The corresponding gender code.
    """
    with open('references/gender_codes.json') as f:
        switch = json.load(f)
    return switch.get(gender)


def growth_rate(rate):
    """
    Accesses dictionary of growth rates.

    :param string rate: The growth rate represented in pokemon.txt.
    :return string: The corresponding growth rate.
    """
    with open('references/growth_rate.json') as f:
        switch = json.load(f)
    return switch.get(rate)


def tm_info(number):
    """
    Accesses dictionary of TM info.

    :param string number: The TM number.
    :return string: The corresponding TM info, in the form "canHaveStab,Type".
    """
    with open('references/tm_info.json') as f:
        switch = json.load(f)
    return switch.get(number)


def move_info(move):
    """
    Accesses dictionary of move info.

    :param string move: The move represented in pokemon.txt and tm.txt in title case.
    :return string: The corresponding move info, in the form "MoveName,canHaveSTAB,type".
    """
    with open('references/move_info.json') as f:
        switch = json.load(f)
    return switch.get(move)


def item_info(item):
    """
    Accesses dictionary of item info.

    :param string item: The held item represented in pokemon.txt.
    :return string: The real, English name of the held item.
    """
    with open('references/item_info.json') as f:
        switch = json.load(f)
    return switch.get(item)


def pokemon_info(dex):
    """
    Accesses dictionary of Pokémon info.

    :param string dex: The dex number relating to the Pokémon.
    :return string: The corresponding Pokémon info, as: "INTERNALNAME, displayName".
    """
    with open('references/pokemon_info.json') as f:
        switch = json.load(f)
    return switch.get(dex)


def location_info(zone):
    """
    Accesses dictionary of location info.

    :param string zone: The numbered zone in terms of a string.
    :return string: The English name of the location the zone belongs to.
    """
    with open('references/location_info.json') as f:
        switch = json.load(f)
    return switch.get(zone)


# endregion


# region Data Collection Methods
def get_pokemon_data(name):
    """
    Given the internal name of a Pokémon, extracts and returns all information in pokemon.txt for that Pokémon.

    :param string name: The internal name of a Pokémon.
    :return dict: A dictionary containing all relevant information found in pokemon.txt.
    """
    with open("gamedata/pokemon.txt", encoding="utf8") as file:
        # Accesses all lines w/o trailing spaces
        line_list = [item.rstrip() for item in file.readlines()]

        # Initialises empty array & bool
        raw_data = []
        found_pokemon = False

        # Iterating through all the pokemon.txt data
        for x in range(0, len(line_list)):

            # Indicates we found the right section of the file. InternalNames are unique.
            if line_list[x] == "InternalName=" + name.upper():
                found_pokemon = True

                # The InternalName line is the 2nd line of the section we care about, grabs the first.
                raw_data = line_list[x-1:x+1]
                continue

            # Now we have found the Pokémon, extract the necessary data
            if found_pokemon:
                raw_data.append(line_list[x])

                # Indicates the start of the next Pokémon's data - stop here
                if "InternalName" in line_list[x]:
                    # Size of Pokémon sections are not constant, but the next InternalName is always 3 lines too far.
                    raw_data.remove(line_list[x])
                    raw_data.remove(line_list[x - 1])
                    raw_data.remove(line_list[x - 2])
                    break

        # Convert into a dictionary of key:value pair for easy access
        # Keys are line starters e.g., "Happiness", values are the associated data, often including commas
        pokemon_dict = {key: value for line in raw_data for key,value in [line.split('=', 1)]}

        # Sound typing is referred to as "Suono" in the game files (Italian)
        if pokemon_dict["Type1"] == "SUONO":
            pokemon_dict["Type1"] = "SOUND"
        if "Type2" in pokemon_dict and pokemon_dict["Type2"] == "SUONO":
            pokemon_dict["Type2"] = "SOUND"

        return pokemon_dict


def get_tm_tutor_data(name):
    """
    Given the internal name of a Pokémon, extracts and returns all information in tm.txt for that Pokémon.

    :param string name: The internal name of a Pokémon.
    :return list|list: The list of TMs learnable, and the list of tutor moves learnable.
    """
    with open("gamedata/tm.txt", encoding="utf8") as file:
        # Accesses all lines w/o trailing spaces
        line_list = [item.rstrip() for item in file.readlines()]

        # Initialise empty arrays
        tm_list = []
        tutor_list = []

        # Iterates through all the TM data, which are contained in lines 5 to 193, every other line being a new move
        for x in range(4, 193, 2):
            # All Pokémon that learn a tm/tutor move are stored on a single, comma-separated line
            names = line_list[x].split(",")

            # Because X or other form pokemon also will contain the same name (e.g.: SHYLEONX has SHYLEON in it),
            # this ensures only exact matches to the given internal name are selected.
            matches = set(names).intersection({name.upper()})

            # If said Pokémon learns any TM moves, add them to the TM list
            if len(matches) > 0:
                tm_list.append(line_list[x - 1].strip("[]"))

        # Everything else is a tutor move, but with random headers and order, so we look at every line
        for x in range(193, len(line_list)):
            names = line_list[x].split(",")
            matches = set(names).intersection({name.upper()})

            # If said Pokémon learns any tutor moves, add them to the tutor list
            if len(matches) > 0:
                tutor_list.append(line_list[x - 1].strip("[]"))

        return tm_list, tutor_list


def get_availability_data(name):
    """
    Given the internal name of a Pokémon, extracts and returns all information in encounters.txt for that Pokémon.

    :param string name: The internal name of a Pokémon.
    :return list|list: The encounter tables for all relevant locations, and the list of zones for those locations.

    :param name:
    :return:
    """
    with open("gamedata/encounters.txt", encoding="utf8") as file:
        line_list = [item.rstrip() for item in file.readlines()]

        encounter_info = []
        found_locations = []
        for x in range(0, len(line_list)):

            # Find first instance of Pokémon's name in a location
            if name.upper() in line_list[x]:
                # Backtrack until we find the start of the route
                end = 0
                start = 0

                # Find the start of the route information
                for a in range(x, 0, -1):
                    start = a
                    if line_list[a] == "#########################":
                        break

                # Find the start of the next route (and therefore end of current)
                for b in range(x + 1, len(line_list), 1):
                    end = b
                    if line_list[b] == "#########################":
                        break

                # Grab the location ID
                loc = line_list[start + 1].split("#")[0].rstrip()

                # If the location has already been processed
                if location_info(loc) in found_locations:
                    continue

                # Mark the location as processed and add the lines to the output
                found_locations.append(location_info(loc))
                encounter_info.append(line_list[start:end])

    return encounter_info, found_locations


# endregion


# region Common Functions
def make_three_digits(digits):
    """
    Converts a string of digits, specifically dex numbers, to a 3-digit string.

    :param string digits: The digits in the form of a string.
    :return string: The given string in 3-digit form.
    """
    # If a 3-digit number is already passed to this function, just return
    if len(digits) == 3:
        return digits

    # Accounts for Alolan/other forms of form "XXX_1" or w/e.
    # The extra "_1" is ignored --> wiki pages never use them
    curr_digits = digits if "_" not in digits else digits.split("_")[0]

    new_digits = ""
    # Add 0s as necessary to make it 3 digits:
    if len(curr_digits) == 1:
        new_digits = "00" + curr_digits
    if len(curr_digits) == 2:
        new_digits = "0" + curr_digits

    return new_digits


def check_values_exists(test_dict, *values):
    """
    Checks if any number of values exist in a given dictionary.

    :param dict test_dict: The dictionary to test.
    :param values: The values that are being looked for.
    :return bool: If specified values are in the given dictionary.
    """
    return all(v in test_dict for v in values)


def find_dex_number(regional_numbers):
    """
    Takes regional numbers from pokemon.txt and convert into a Pokédex number of e.g., "X031".

    :param string regional_numbers: The regional numbers for a Pokémon in pokemon.txt.
    :return string: The (global) dex number for the Pokémon.
    """
    # Regional numbers are in form "X,Y,Z", where X is normal dex, Y is xeno dex, Z is vintage dex
    # Every Pokémon only has 1 non-zero regional number
    if regional_numbers.split(",")[0] != "0":
        dex_nums = make_three_digits(regional_numbers.split(",")[0])
    elif regional_numbers.split(",")[1] != "0":
        # For some reason, X030 just doesn't exist in the game's data. As Pokédex numbers are only used for wiki display
        # anyway, I'm just going to manually adjust these numbers and keep w/ the X030 = Mewtwo X wiki system
        if int(regional_numbers.split(",")[1]) > 29:
            dex_nums = "X" + make_three_digits(str(int(regional_numbers.split(",")[1]) - 1))
        else:
            dex_nums = "X" + make_three_digits(regional_numbers.split(",")[1])
    else:
        dex_nums = "V" + make_three_digits(regional_numbers.split(",")[2])

    return dex_nums


# endregion


# region Create Wiki Elements
def create_header_footer(pokemon_dict):
    """
    Creates the header/footer for the Pokémon given relevant information.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :return list[str]: The wiki code to produce the header/footer.
    """
    head_foot = ["{{PokemonPrevNextHead", "|type = " + pokemon_dict["Type1"].title()]

    # Typing
    if "Type2" in pokemon_dict:
        head_foot.append("|type2 = " + pokemon_dict["Type2"].title())

    # Get the dex number of the current Pokémon
    dex_num = find_dex_number(pokemon_dict["RegionalNumbers"])

    if dex_num[0] == "X":
        num = dex_num[1:4]
        if int(num) > 1:
            head_foot.append("|prev = " + pokemon_info("X" + make_three_digits(str(int(num) - 1))).split(",")[1])
            head_foot.append("|prevnum = X" + make_three_digits(str(int(num) - 1)))
        else:
            head_foot.append("|prev = " + pokemon_info("583").split(",")[1])
            head_foot.append("|prevnum = 583")
        if int(num) < 44:
            head_foot.append("|next = " + pokemon_info("X" + make_three_digits(str(int(num) + 1))).split(",")[1])
            head_foot.append("|nextnum = X" + make_three_digits(str(int(num) + 1)))
        else:
            head_foot.append("|next = " + pokemon_info("V001").split(",")[1])
            head_foot.append("|nextnum = V001")
    elif dex_num[0] == "V":
        num = dex_num[1:4]
        if int(num) > 1:
            head_foot.append("|prev = " + pokemon_info("V" + make_three_digits(str(int(num) - 1))).split(",")[1])
            head_foot.append("|prevnum = V" + make_three_digits(str(int(num) - 1)))
        else:
            head_foot.append("|prev = " + pokemon_info("X044").split(",")[1])
            head_foot.append("|prevnum = X044")
        if int(num) < 207:
            head_foot.append("|next = " + pokemon_info("V" + make_three_digits(str(int(num) + 1))).split(",")[1])
            head_foot.append("|nextnum = V" + make_three_digits(str(int(num) + 1)))
    else:
        num = dex_num[:3]
        if int(num) > 1:
            head_foot.append("|prev = " + pokemon_info(make_three_digits(str(int(num) - 1))).split(",")[1])
            head_foot.append("|prevnum = " + make_three_digits(str(int(num) - 1)))
        if int(num) < 583:
            head_foot.append("|next = " + pokemon_info(make_three_digits(str(int(num) + 1))).split(",")[1])
            head_foot.append("|nextnum = " + make_three_digits(str(int(num) + 1)))
        else:
            head_foot.append("|next = " + pokemon_info("X001").split(",")[1])
            head_foot.append("|nextnum = X001")

    head_foot.append("}}")

    return head_foot


def create_infobox(pokemon_dict):
    """
    Creates the infobox for the Pokémon given relevant information.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :return list[str]: The wiki code to produce the infobox.
    """
    # Initialise the infobox
    infobox = ["{{Pokemon Infobox", "|type1 = " + pokemon_dict["Type1"].title()]

    # Typing for colouring
    if "Type2" in pokemon_dict:
        infobox.append("|type2 = " + pokemon_dict["Type2"].title())

    # Name, Species
    dex_data = pokemon_info(find_dex_number(pokemon_dict["RegionalNumbers"]))
    infobox.append("|name = " + dex_data.split(",")[1])
    infobox.append("|species = Species Name")

    # Dex & Image
    dex_nums = find_dex_number(pokemon_dict["RegionalNumbers"])
    infobox.append("|ndex = " + dex_nums)
    infobox.append("|image = " + pokemon_dict["Name"] + ".png")

    # Abilities
    reg_abilities = pokemon_dict["Abilities"].split(",")
    infobox.append("|ability1 = " + reg_abilities[0].title())
    if len(reg_abilities) > 1:
        infobox.append("|ability2 = " + reg_abilities[1].title())
    if "HiddenAbility" in pokemon_dict:
        infobox.append("|hiddenability = " + pokemon_dict["HiddenAbility"].title())

    # Gender, Catch Rate
    infobox.append("|gendercode = " + gender_code(pokemon_dict["GenderRate"]))
    infobox.append("|catchrate = " + pokemon_dict["Rareness"])

    # Egg Groups & Steps
    egg_groups = pokemon_dict["Compatibility"].split(",")
    infobox.append("|egggroup1 = " + egg_groups[0])
    if len(egg_groups) > 1:
        infobox.append("|egggroup2 = " + egg_groups[1])
    infobox.append("|eggsteps = " + pokemon_dict["StepsToHatch"])

    # Metric height & weight
    infobox.append("|height-m = " + str(int(pokemon_dict["Height"]) / 10))
    infobox.append("|weight-kg = " + str(int(pokemon_dict["Weight"]) / 10))

    # Exp Yield & Level Rate
    infobox.append("|expyield = " + pokemon_dict["BaseEXP"])
    infobox.append("|lvrate = " + growth_rate(pokemon_dict["GrowthRate"]))

    # Colour & Friendship
    infobox.append("|color = " + pokemon_dict["Color"])
    infobox.append("|friendship = " + pokemon_dict["Happiness"])

    # EVs
    evs = pokemon_dict["EffortPoints"].split(",")
    if evs[0] != "0":
        infobox.append("|evhp = " + evs[0])
    if evs[1] != "0":
        infobox.append("|evat = " + evs[1])
    if evs[2] != "0":
        infobox.append("|evde = " + evs[2])
    if evs[3] != "0":
        infobox.append("|evsp = " + evs[3])
    if evs[4] != "0":
        infobox.append("|evsa = " + evs[4])
    if evs[5] != "0":
        infobox.append("|evsd = " + evs[5])

    # Closing brackets
    infobox.append("}}")

    return infobox


def create_opening_paragraph(pokemon_dict):
    """
    Creates the opening paragraph for the Pokémon given relevant information.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :return list[str]: The wiki code to produce the opening paragraph.
    """
    opening_paragraph = []

    # "dual-type" prefixes Pokémon of two types.
    dual_type = "dual-type" if "Type2" in pokemon_dict else ""

    # Creates the relevant type description & link
    typing = "{{Type|" + pokemon_dict["Type1"].title() + "}}/{{Type|" + pokemon_dict["Type2"].title(
    ) + "}}" if "Type2" in pokemon_dict else "{{Type|" + pokemon_dict["Type1"].title() + "}}"

    # First line
    opening_paragraph.append(
        f"'''{pokemon_dict['Name']}''' is a {dual_type} {typing}-type Pokémon.")

    return opening_paragraph


# Really no way to do this without knowing italian, just here for posterity
def create_pokedex_entry(pokemon_dict):
    """
    Currently incomplete; just creates an empty Pokédex entry.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :return list[str]: The wiki code to produce the Pokédex entry.
    """
    pokedex_entry = ["{{Dex", "|type = " + pokemon_dict["Type1"].title()]

    if "Type2" in pokemon_dict:
        pokedex_entry.append("|type2 = " + pokemon_dict["Type2"].title())
    pokedex_entry.append("''WIP''")
    pokedex_entry.append("}}")

    return pokedex_entry


def create_game_locations(pokemon_dict, locations, loc_numbers):
    # Collection of location states, which is the type of encounter area
    location_states = ["Cave", "Water", "OldRod", "GoodRod", "SuperRod", "LandDay", "LandNight", "RockSmash", "Land"]

    # Start game location box
    game_locations = ["{{Availability", "|type = " + pokemon_dict["Type1"].title()]
    if "Type2" in pokemon_dict:
        game_locations.append("|type2 = " + pokemon_dict["Type2"].title())

    # If no wild encounters, the Pokémon is static only or evolution only or breeding only
    if len(locations) == 0:
        game_locations.append("|none = WIP")
    else:
        # Initialises lists to hold encounter information for the three different rarities
        enc_common = []
        enc_uncommon = []
        enc_rare = []

        # For every location the Pokémon is present
        z = 0
        for loc in locations:
            # Initialises an array
            state_indexes = []

            # Find the indexes of the different states in a particular location
            for x in range(0, len(loc)):
                if loc[x] in location_states:
                    state_indexes.append(x)

            # Creates a dictionary
            loc_dict = {}

            # Not fully sure, but the case of len() = 1 needs to be handled individually
            if len(state_indexes) == 1:
                loc_dict[loc[state_indexes[0]]] = loc[state_indexes[0]+1:]
            # Otherwise, adds the states as a key to the dictionary with the lines under it as a value
            else:
                for n in range(0, len(state_indexes)-1, 2):
                    loc_dict[loc[state_indexes[n]]] = loc[state_indexes[n]+1:state_indexes[n+1]]

            for state in loc_dict.items():
                # The Pokémon is not necessarily in every state in each location
                try:
                    # Extracts all the indexes where the Pokémon is located in a certain state
                    # Each index corresponds to a certain percentage, and if a Pokémon appears at multiple those
                    # percentages are added to find the final encounter chance.
                    indexes = [i for i, e in enumerate(state[1]) if pokemon_dict["InternalName"] in e]
                    if not indexes:
                        continue

                    secondary_information = ""

                    percentage = 0
                    if state[0] in ["Land", "LandDay", "LandNight", "Cave"]:
                        for index in indexes:
                            if index in [1, 2]:
                                percentage += 20
                            elif index in [3, 4, 5, 6]:
                                percentage += 10
                            elif index in [7, 8]:
                                percentage += 5
                            elif index in [9, 10]:
                                percentage += 4
                            else:
                                percentage += 1

                        if state[0] == "LandDay":
                            secondary_information = "Day"
                        elif state[0] == "LandNight":
                            secondary_information = "Night"

                    elif state[0] in ["RockSmash", "Water"]:
                        for index in indexes:
                            if index in [1]:
                                percentage += 60
                            elif index in [2]:
                                percentage += 30
                            elif index in [3]:
                                percentage += 5
                            elif index in [4]:
                                percentage += 4
                            else:
                                percentage += 1

                        if state[0] == "RockSmash":
                            secondary_information = "Rock Smash"
                        else:
                            secondary_information = "Surf"

                    elif state[0] == "OldRod":
                        for index in indexes:
                            if index in [1]:
                                percentage += 70
                            else:
                                percentage += 30

                        secondary_information = "Old Rod"

                    elif state[0] == "GoodRod":
                        for index in indexes:
                            if index in [1]:
                                percentage += 60
                            else:
                                percentage += 20

                        secondary_information = "Good Rod"

                    # note: this is SuperRod
                    else:
                        for index in indexes:
                            if index in [1]:
                                percentage += 40
                            elif index in [2]:
                                percentage += 30
                            elif index in [3]:
                                percentage += 15
                            elif index in [4]:
                                percentage += 10
                            else:
                                percentage += 5

                        secondary_information = "Super Rod"

                    #
                    loc_data = loc_numbers[z]

                    route_string = "[[" + loc_data + "]] (" + secondary_information + ")" \
                        if secondary_information != "" else "[[" + loc_data + "]]"
                    if percentage > 15:
                        enc_common.append(route_string)
                    elif percentage > 5:
                        enc_uncommon.append(route_string)
                    else:
                        enc_rare.append(route_string)

                # ValueError is raised if they can't find the name, so the Pokémon isn't in that state
                except ValueError:
                    continue

            #
            z += 1

        #
        if len(enc_common) > 0:
            game_locations.append("|common = " + ", ".join(enc_common))
        if len(enc_uncommon) > 0:
            game_locations.append("|uncommon = " + ", ".join(enc_uncommon))
        if len(enc_rare) > 0:
            game_locations.append("|rare = " + ", ".join(enc_rare))

    game_locations.append("}}")

    return game_locations


def create_wild_items(pokemon_dict):
    """
    Creates the wild held item box for the Pokémon given relevant information.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :return list[str]: The wiki code to produce the wild held item box.
    """
    # Initialise the box
    wild_items = ["{{HeldItems", "|type = " + pokemon_dict["Type1"].title()]

    # Type colouring
    if "Type2" in pokemon_dict:
        wild_items.append("|type2 = " + pokemon_dict["Type2"].title())

    # If the same item is listed in all slots, it indicates the Pokémon will always have that item
    if (check_values_exists(pokemon_dict, "WildItemCommon", "WildItemUncommon", "WildItemRare")
            and (pokemon_dict["WildItemCommon"] == pokemon_dict["WildItemUncommon"]
                 and pokemon_dict["WildItemUncommon"] == pokemon_dict["WildItemRare"])):
        item = item_info(pokemon_dict["WildItemCommon"])
        wild_items.append("|always = {{Item|" + item + "}} [[" + item + "]]")

    # Otherwise, adds the relevant information as necessary
    else:
        if "WildItemCommon" in pokemon_dict:
            item = item_info(pokemon_dict["WildItemCommon"])
            wild_items.append("|common = {{Item|" + item + "}} [[" + item + "]]")
        if "WildItemUncommon" in pokemon_dict:
            item = item_info(pokemon_dict["WildItemUncommon"])
            wild_items.append("|uncommon = {{Item|" + item + "}} [[" + item + "]]")
        if "WildItemRare" in pokemon_dict:
            item = item_info(pokemon_dict["WildItemRare"])
            wild_items.append("|rare = {{Item|" + item + "}} [[" + item + "]]")

    # Close box
    wild_items.append("}}")

    return wild_items


def create_stats(pokemon_dict):
    """
    Creates the stats box for the Pokémon given relevant information.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :return list[str]: The wiki code to produce the stats box.
    """
    # Initialises the stats box
    stats = ["{{Stats", "|type = " + pokemon_dict["Type1"].title()]

    if "Type2" in pokemon_dict:
        stats.append("|type2 = " + pokemon_dict["Type2"].title())

    # Stats are given in HP/ATK/DEF/SPE/SPA/SPD
    raw_stats = pokemon_dict["BaseStats"].split(",")
    stats.append("|HP = " + raw_stats[0])
    stats.append("|Attack = " + raw_stats[1])
    stats.append("|Defense = " + raw_stats[2])
    stats.append("|SpAtk = " + raw_stats[4])
    stats.append("|SpDef = " + raw_stats[5])
    stats.append("|Speed = " + raw_stats[3])

    stats.append("}}")

    return stats


# Going to have to fill this in manually
def create_type_effectiveness(pokemon_dict):
    """
    Incomplete, creates an empty type effectiveness box.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :return list[str]: The wiki code to produce the type effectiveness box.
    """
    type_effectiveness = ["{{TypeEffectiveness", "|type1 = " + pokemon_dict["Type1"].title()]

    if "Type2" in pokemon_dict:
        type_effectiveness.append("|type2 = " + pokemon_dict["Type2"].title())
    type_effectiveness.append("}}")

    return type_effectiveness


def create_level_learn_list(pokemon_dict):
    """
    Creates the level learn list for the Pokémon given relevant information.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :return list[str]: The wiki code to produce the level learn list.
    """
    # Box colouring a bit different for move boxes, second type is either unique or the first type repeated
    second_type = pokemon_dict["Type2"].title() if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    # Create the start of the level learn box.
    dex_data = pokemon_info(find_dex_number(pokemon_dict["RegionalNumbers"]))
    level_learn_list = ["{{MoveLevelStart|" + dex_data.split(",")[1] + "|" + pokemon_dict["Type1"].title() + "|"
                        + second_type + "}}"]

    # Learners are stored in a comma-separated single line.
    moves = pokemon_dict["Moves"].split(",")

    # Stored in the form: level, MOVENAME; so new move information only starts on every other line.
    for x in range(0, len(moves) - 1, 2):
        # Gets the related data from move_info.json
        move_data = move_info(moves[x + 1]).split(",")

        # Adds moves to the box, accounting for STAB, and using the real name from the JSON file
        if move_data[1] == "yes" and (move_data[2] == pokemon_dict["Type1"].title() or move_data[2] == second_type):
            level_learn_list.append("{{MoveLevel+|" + moves[x] + "|" + move_data[0] + "|'''}}")
        else:
            level_learn_list.append("{{MoveLevel+|" + moves[x] + "|" + move_data[0] + "}}")

    level_learn_list.append("{{MoveLevelEnd|" + dex_data.split(",")[1] + "|" + pokemon_dict["Type1"].title() + "|"
                            + second_type + "}}")

    return level_learn_list


def create_tm_learn_list(pokemon_dict, tm_list):
    """
    Creates the TM learn list for the Pokémon given relevant information.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :param list[str] tm_list: The list of TMs the Pokémon can learn.
    :return list[str]: The wiki code to produce the TM learn list.
    """
    # Box colouring a bit different for move boxes, second type is either unique or the first type repeated
    second_type = pokemon_dict["Type2"].title() if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    # Initialises the TM box
    dex_data = pokemon_info(find_dex_number(pokemon_dict["RegionalNumbers"]))
    tm_learn_list = ["{{MoveTMStart|" + dex_data.split(",")[1] + "|" + pokemon_dict["Type1"].title() + "|"
                     + second_type + "}}"]

    # tm_list contains every TM teachable to this Pokémon
    for move in tm_list:
        # Gets the related data from move_info.json
        tm_data = tm_info(move).split(",")

        # Adds the move to the box accounting for STAB. TMs use TM number, not the name of the move
        if (tm_data[1] == "yes") and (tm_data[2] == pokemon_dict["Type1"].title() or tm_data[2] == second_type):
            tm_learn_list.append("{{MoveTM+|TM" + tm_data[0] + "|'''}}")
        else:
            tm_learn_list.append("{{MoveTM+|TM" + tm_data[0] + "}}")

    tm_learn_list.append("{{MoveTMEnd|" + dex_data.split(",")[1] + "|" + pokemon_dict["Type1"].title() + "|"
                         + second_type + "}}")

    return tm_learn_list


def create_breeding_learn_list(pokemon_dict):
    """
    Creates the breeding learn list for the Pokémon given relevant information. N.b., breeding moves and egg moves mean
    the same thing; but the former is preferred for the wiki, and the latter is preferred in game data.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :return list[str]: The wiki code to produce the breeding learn list.
    """
    # Box colouring a bit different for move boxes, second type is either unique or the first type repeated
    second_type = pokemon_dict["Type2"].title() if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    # Initialises the breeding move box
    dex_data = pokemon_info(find_dex_number(pokemon_dict["RegionalNumbers"]))
    breeding_learn_list = ["{{MoveBreedStart|" + dex_data.split(",")[1] + "|" + pokemon_dict["Type1"].title() +
                           "|" + second_type + "}}"]

    # Not every Pokémon, especially evolutions/legendaries, have egg moves
    if "EggMoves" in pokemon_dict:
        # Egg moves are stored together on one line, separated by commas
        egg_moves = pokemon_dict["EggMoves"].split(",")

        # All Field egg group Pokémon can get every egg move from Smeargle father, indicated here
        breed_string = "{{EM|107|Smeargle}} '''WIP'''" if "Field" in pokemon_dict["Compatibility"] else "'''WIP'''"

        # Initialise array to hold the real names of the egg moves
        breeding_moves = []

        for move in egg_moves:
            # Gets the related data from move_info.json
            move_data = move_info(move).split(",")

            # Adds to the breeding moves array accounting for STAB
            if (move_data[1] == "yes") and (
                    move_data[2] == pokemon_dict["Type1"].title() or move_data[2] == second_type):
                breeding_moves.append("{{MoveBreed+|" + breed_string + "|" + move_data[0] + "|'''}}")
            else:
                breeding_moves.append("{{MoveBreed+|" + breed_string + "|" + move_data[0] + "}}")

        # Egg moves are stored in odd orders in the game data, this sorts them alphabetically.
        for line in sorted(breeding_moves):
            breeding_learn_list.append(line)

    # Otherwise, indicate there are no egg moves
    else:
        breeding_learn_list.append("{{MoveBreedNone}}")

    breeding_learn_list.append("{{MoveBreedEnd|" + dex_data.split(",")[1] + "|" + pokemon_dict["Type1"].title() +
                               "|" + second_type + "}}")

    return breeding_learn_list


def create_tutor_learn_list(pokemon_dict, tutor_list):
    """
    Creates the tutor learn list for the Pokémon given relevant information.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :param list[str] tutor_list: The list of tutor moves the Pokémon can learn.
    :return list[str]: The wiki code to produce the tutor learn list.
    """
    # Box colouring a bit different for move boxes, second type is either unique or the first type repeated
    second_type = pokemon_dict["Type2"].title() if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    # Initialises the tutor learn list box
    dex_data = pokemon_info(find_dex_number(pokemon_dict["RegionalNumbers"]))
    tutor_learn_list = ["{{MoveTutorStart|" + dex_data.split(",")[1] + "|" + pokemon_dict["Type1"].title() + "|" +
                        second_type + "}}"]

    tutor_moves = []
    for move in tutor_list:
        # Gets the relevant information from move_info.json
        move_data = move_info(move).split(",")

        # Adds to tutor moves account for STAB. Tutor price is a column currently not utilised, but "Varies" is used
        if (move_data[1] == "yes") and (move_data[2] == pokemon_dict["Type1"].title() or move_data[2] == second_type):
            tutor_moves.append("{{MoveTutor+|" + move_data[0] + "|'''|Varies}}")
        else:
            tutor_moves.append("{{MoveTutor+|" + move_data[0] + "||Varies}}")

    # Similarly to egg moves, tutor moves are not in any order; we choose alphabetical
    for line in sorted(tutor_moves):
        tutor_learn_list.append(line)

    tutor_learn_list.append("{{MoveTutorEnd|" + dex_data.split(",")[1] + "|" + pokemon_dict["Type1"].title() + "|"
                            + second_type + "}}")

    return tutor_learn_list


def create_sprites(pokemon_dict):
    """
    Creates the sprite string for the Pokémon given relevant information.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :return list[str]: The wiki code to produce the sprite string.
    """
    second_type = pokemon_dict["Type2"].title() if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    dex_data = pokemon_info(find_dex_number(pokemon_dict["RegionalNumbers"]))
    sprites = ("{{sprites|name=" + dex_data.split(",")[1] + "|type=" + pokemon_dict["Type1"].title() + "|type2=" +
               second_type + "}}")

    return sprites
# endregion


def main():
    # Get the name of the Pokémon for the wiki page
    internal_name = input("\nInput the name of the pokemon: ")

    # Get pokemon, move, and location data
    pokemon_data = get_pokemon_data(internal_name)
    tm_data, tutor_data = get_tm_tutor_data(internal_name)
    location_data, loc_nums = get_availability_data(internal_name)

    # Create the necessary components of the pokemon wiki page
    header_footer = create_header_footer(pokemon_data)
    info_box = create_infobox(pokemon_data)
    open_para = create_opening_paragraph(pokemon_data)
    dex_entry = create_pokedex_entry(pokemon_data, )
    availability = create_game_locations(pokemon_data, location_data, loc_nums)
    held_items = create_wild_items(pokemon_data)
    base_stats = create_stats(pokemon_data)
    type_eff = create_type_effectiveness(pokemon_data)
    level_learn_set = create_level_learn_list(pokemon_data)
    tm_learn_set = create_tm_learn_list(pokemon_data, tm_data)
    egg_learn_set = create_breeding_learn_list(pokemon_data)
    tutor_learn_set = create_tutor_learn_list(pokemon_data, tutor_data)
    sprite_string = create_sprites(pokemon_data)

    # Adding it all together
    wiki_page = []

    for line in header_footer:
        wiki_page.append(str(line))
    for line in info_box:
        wiki_page.append(str(line))
    for line in open_para:
        wiki_page.append(str(line))
    # Need to add evolution line here

    wiki_page.append("")
    wiki_page.append("")
    wiki_page.append("")

    wiki_page.append("=='''Pokédex entries'''==")
    for line in dex_entry:
        wiki_page.append(str(line))

    wiki_page.append("=='''Game locations'''==")
    for line in availability:
        wiki_page.append(str(line))

    wiki_page.append("=='''Held items'''==")
    for line in held_items:
        wiki_page.append(str(line))

    wiki_page.append("=='''Stats'''==")
    for line in base_stats:
        wiki_page.append(str(line))

    wiki_page.append("=='''Type effectiveness'''==")
    for line in type_eff:
        wiki_page.append(str(line))

    wiki_page.append("=='''Learnset'''==")
    wiki_page.append("==='''By leveling up'''===")
    for line in level_learn_set:
        wiki_page.append(str(line))

    wiki_page.append("==='''By TM/HM'''===")
    for line in tm_learn_set:
        wiki_page.append(str(line))

    wiki_page.append("==='''By breeding'''===")
    for line in egg_learn_set:
        wiki_page.append(str(line))

    wiki_page.append("==='''By tutoring'''===")
    for line in tutor_learn_set:
        wiki_page.append(str(line))

    wiki_page.append("=='''Sprites'''==")
    wiki_page.append(sprite_string)

    wiki_page.append("")
    wiki_page.append("")
    for line in header_footer:
        wiki_page.append(str(line))

    for line in wiki_page:
        print(line)


if __name__ == "__main__":

    while True:
        try:
            main()
        except Exception:
            print("")
            logging.error(traceback.format_exc())
            print("\nPlease contact @Siphlygon on Discord or on the Pokémon Xenoverse Wiki with the printed error message")
            input("Press any key to close this script.")
            exit()
