# -*- coding: utf-8 -*-
# pylint: disable=locally-disabled, too-many-lines, line-too-long
"""
Create Pokémon page script for the Pokémon Xenoverse Wiki.

Reads in a given internal name matching a Pokémon in the game data for Pokémon Xenoverse. Contains a copy of the
relevant game files for use and access, and a set of custom reference dictionaries matching strings in the game data to
associated information.

Prints lines in the style of the Pokémon Xenoverse Wiki code. These can be copied and pasted straight onto the wiki page
and will render correctly.

Elements still to implement:
- header & footer
- availability
  * including wild encounters
  * and static encounters
- egg move fathers
- evolution
  * in the evolution box at the end of the page
  * in indicating future STAB in the move learn lists
  * in the opening paragraph box
- pokédex entries (may not be possible in English)
- separate forms (may choose not to implement)

@author: Siphlygon
Last Updated: 18th March 2024
"""

import json


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
                raw_data = line_list[x-1:x]
                continue

            # Now we have found the Pokémon, extract the necessary data
            if found_pokemon:
                raw_data.append(line_list[x])

                # Indicates the start of the next Pokémon's data - stop here
                if "InternalName" in line_list[x]:
                    # Size of Pokémon sections are not constant, but the next InternalName is always 3 lines too far.
                    raw_data.remove(line_list[x])
                    raw_data.remove(line_list[x-1])
                    raw_data.remove(line_list[x-2])
                    break

        # Convert into a dictionary of key:value pair for easy access
        # Keys are line starters e.g., "Happiness", values are the associated data, often including commas
        pokemon_dict = {key: value for line in raw_data for key,
                        value in [line.split('=', 1)]}

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

        # Iterating through all the tm.txt data
        for x in range(4, len(line_list)):
            names = line_list[x].split(",")

            matches = set(names).intersection({name.upper()})
            if len(matches) > 0:

                # The highest TM is dark pulse, at 95
                if ((x/2) - 1) < 96:
                    if (x/2 - 1) // 10 > 0:
                        tm_list.append(str(int((x/2) - 1)))
                    else:
                        tm_list.append("0" + str(int((x/2) - 1)))

                # Otherwise, it can only be taught at move tutor
                else:
                    tutor_list.append(line_list[x-1].strip("[]").title())

        return tm_list, tutor_list
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
# endregion


# region Create Wiki Elements
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
    infobox.append("|name = " + pokemon_dict["Name"])
    infobox.append("|species = " + pokemon_dict["Kind"])

    # Dex & Image
    dex_nums = pokemon_dict["RegionalNumbers"].split(",")
    if dex_nums[0] != "0":
        infobox.append("|ndex = " + make_three_digits(dex_nums[0]))
    elif dex_nums[1] != "0":
        infobox.append("|ndex = X" + make_three_digits(dex_nums[0]))
    else:
        infobox.append("|ndex = V" + make_three_digits(dex_nums[0]))
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
    infobox.append("|height-m = " + str(int(pokemon_dict["Height"])/10))
    infobox.append("|weight-kg = " + str(int(pokemon_dict["Weight"])/10))

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
        item = item_info(pokemon_dict["WildItemCommon"].title())
        wild_items.append("|always = {{Item|" + item + "}} [[" + item + "]]")

    # Otherwise, adds the relevant information as necessary
    else:
        if "WildItemCommon" in pokemon_dict:
            item = item_info(pokemon_dict["WildItemCommon"].title())
            wild_items.append("|common = {{Item|" + item + "}} [[" + item + "]]")
        if "WildItemUncommon" in pokemon_dict:
            item = item_info(pokemon_dict["WildItemUncommon"].title())
            wild_items.append("|uncommon = {{Item|" + item + "}} [[" + item + "]]")
        if "WildItemRare" in pokemon_dict:
            item = item_info(pokemon_dict["WildItemRare"].title())
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
    level_learn_list = ["{{MoveLevelStart|" + pokemon_dict["Name"].title() + "|" + pokemon_dict["Type1"].title() + "|"
                        + second_type + "}}"]

    # Learners are stored in a comma-separated single line.
    moves = pokemon_dict["Moves"].split(",")

    # Stored in the form: level, MOVENAME; so new move information only starts on every other line.
    for x in range(0, len(moves)-1, 2):
        # Gets the related data from move_info.json
        move_data = move_info(moves[x+1].title()).split(",")

        # Adds moves to the box, accounting for STAB, and using the real name from the JSON file
        if move_data[1] == "yes" and (move_data[2] == pokemon_dict["Type1"].title() or move_data[2] == second_type):
            level_learn_list.append("{{MoveLevel+|" + moves[x] + "|" + move_data[0] + "|'''}}")
        else:
            level_learn_list.append("{{MoveLevel+|" + moves[x] + "|" + move_data[0] + "}}")

    level_learn_list.append("{{MoveLevelEnd|" + pokemon_dict["Name"].title() + "|" + pokemon_dict["Type1"].title() + "|"
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
    tm_learn_list = ["{{MoveTMStart|" + pokemon_dict["Name"].title() + "|" + pokemon_dict["Type1"].title() + "|"
                     + second_type + "}}"]

    # tm_list contains every TM teachable to this Pokémon
    for num in tm_list:
        # Gets the related data from move_info.json
        tm_data = tm_info(num).split(",")

        # Adds the move to the box accounting for STAB. TMs use TM number, not the name of the move
        if (tm_data[0] == "yes") and (tm_data[1] == pokemon_dict["Type1"].title() or tm_data[1] == second_type):
            tm_learn_list.append("{{MoveTM+|TM" + num + "|'''}}")
        else:
            tm_learn_list.append("{{MoveTM+|TM" + num + "}}")

    tm_learn_list.append("{{MoveTMEnd|" + pokemon_dict["Name"].title() + "|" + pokemon_dict["Type1"].title() + "|"
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

    breeding_learn_list = ["{{MoveBreedStart|" + pokemon_dict["Name"].title() + "|" + pokemon_dict["Type1"].title() +
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
            move_data = move_info(move.title()).split(",")

            # Adds to the breeding moves array accounting for STAB
            if (move_data[1] == "yes") and (move_data[2] == pokemon_dict["Type1"].title() or move_data[2] == second_type):
                breeding_moves.append("{{MoveBreed+|" + breed_string + "|" + move_data[0] + "|'''}}")
            else:
                breeding_moves.append("{{MoveBreed+|" + breed_string + "|" + move_data[0] + "}}")

        # Egg moves are stored in odd orders in the game data, this sorts them alphabetically.
        for line in sorted(breeding_moves):
            breeding_learn_list.append(line)

    # Otherwise, indicate there are no egg moves
    else:
        breeding_learn_list.append("{{MoveBreedNone}}")

    breeding_learn_list.append("{{MoveBreedEnd|" + pokemon_dict["Name"].title() + "|" + pokemon_dict["Type1"].title() +
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

    tutor_learn_list = ["{{MoveTutorStart|" + pokemon_dict["Name"].title() + "|" + pokemon_dict["Type1"].title() + "|" +
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

    tutor_learn_list.append("{{MoveTutorEnd|" + pokemon_dict["Name"].title() + "|" + pokemon_dict["Type1"].title() + "|"
                            + second_type + "}}")

    return tutor_learn_list


def create_sprites(pokemon_dict):
    """
    Creates the sprite string for the Pokémon given relevant information.

    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :return list[str]: The wiki code to produce the sprite string.
    """
    second_type = pokemon_dict["Type2"].title() if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    sprites = ("{{sprites|name=" + pokemon_dict["Name"].title() + "|type=" + pokemon_dict["Type1"].title() + "|type2=" +
               second_type + "}}")

    return sprites
# endregion


def main():
    # Get the name of the Pokémon for the wiki page
    internal_name = input("\nInput the name of the pokemon: ")

    # Get pokemon, move, and location data
    pokemon_data = get_pokemon_data(internal_name)
    tm_data, tutor_data = get_tm_tutor_data(internal_name)

    # Create the necessary components of the pokemon wiki page
    info_box = create_infobox(pokemon_data)
    open_para = create_opening_paragraph(pokemon_data)
    dex_entry = create_pokedex_entry(pokemon_data,)
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

    for line in wiki_page:
        print(line)


if __name__ == "__main__":

    while True:
        main()
