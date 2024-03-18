# -*- coding: utf-8 -*-
# pylint: disable=locally-disabled, too-many-lines
"""
Created on Sat Mar 16 00:03:52 2024

@author: Siphlygon
"""

import json


def gender_code(gender):
    """
    Accesses dictionary of gender codes.

    Args:
        gender (string): The gender represented in pokemon.txt

    Returns:
        string: The corresponding gender code.
    """
    with open('references/gender_codes.json') as f:
        switch = json.load(f)
    return switch.get(gender)


def growth_rate(rate):
    """
    Accesses dictionary of growth rates.

    Args:
        rate (string): The growth rate represented in pokemon.txt

    Returns:
        string: The corresponding growth rate.
    """
    with open('references/growth_rate.json') as f:
        switch = json.load(f)
    return switch.get(rate)


def tm_info(number):
    """
    Accesses dictionary of TM info.

    Args:
        number (string): The TM number

    Returns:
        string: canHaveStab,Type
    """
    with open('references/tm_info.json') as f:
        switch = json.load(f)
    return switch.get(number)


def move_info(move):
    """
    Accesses dictionary of moves.

    Args:
        move (string): The move represented in pokemon.txt and tm.txt in title case.

    Returns:
        string: MoveName,canHaveSTAB,type
    """
    with open('references/move_info.json') as f:
        switch = json.load(f)
    return switch.get(move)


def item_info(item):
    """
    Accesses dictionary of held items.

    Args:
        item (string): The held item represented in pokemon.txt

    Returns:
        string: The real, English name of the held item.
    """
    with open('references/item_info.json') as f:
        switch = json.load(f)
    return switch.get(item)

# region Data Collection Methods
def get_pokemon_data(name):
    """Given the internal name of a Pokémon, extracts and returns all information in pokemon.txt for
    that Pokémon.

    Args:
        name (string): The internal name of a Pokémon.

    Returns:
        dict: A dictionary containing all relevant information in pokemon.txt
    """

    with open("gamedata/pokemon.txt", encoding="utf8") as file:
        # Grabs the line
        line_list = [item.rstrip() for item in file.readlines()]

        # Contains all the lines including data about the Pokémon
        raw_data = []

        found_pokemon = False
        for x in range(0, len(line_list)):

            # Found the Pokémon we're looking for and it's related data
            if line_list[x] == "InternalName=" + name.upper():
                found_pokemon = True
                raw_data = line_list[x-1:x]
                continue

            # Now we have found the Pokémon, extract the necessary data
            if found_pokemon:
                raw_data.append(line_list[x])

                # Indicates the start of the next Pokémon's data - stop here
                if "InternalName" in line_list[x]:
                    found_pokemon = False
                    raw_data.remove(line_list[x])
                    raw_data.remove(line_list[x-1])
                    raw_data.remove(line_list[x-2])
                    break

        # Convert into a dictionary of key:value pair for easy access
        pokemon_dict = {key: value for line in raw_data for key,
                        value in [line.split('=', 1)]}

        if pokemon_dict["Type1"] == "SUONO":
            pokemon_dict["Type1"] = "SOUND"
        if "Type2" in pokemon_dict:
            if pokemon_dict["Type2"] == "SUONO":
                pokemon_dict["Type2"] = "SOUND"

        return pokemon_dict


def get_tm_tutor_data(name):

    with open("gamedata/tm.txt", encoding="utf8") as file:
        # Grabs the line
        line_list = [item.rstrip() for item in file.readlines()]

        # Contains all the lines including data about the Pokémon
        tm_list = []
        tutor_list = []

        for x in range(0, len(line_list)):
            names = line_list[x].split(",")

            matches = set(names).intersection(set([name.upper()]))
            # If a TM, adds TM num & name
            # if name.upper() in line_list[x]:
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

# region Create Wiki Elements
def create_infobox(pokemon_dict):
    infobox = []

    infobox.append("{{Pokemon Infobox")

    # Typing
    infobox.append("|type1 = " + pokemon_dict["Type1"].title())
    if "Type2" in pokemon_dict:
        infobox.append("|type2 = " + pokemon_dict["Type2"].title())

    # Name, Species
    infobox.append("|name = " + pokemon_dict["Name"])
    infobox.append("|species = " + pokemon_dict["Kind"])

    # Dex & Image
    dex_nums = pokemon_dict["RegionalNumbers"].split(",")
    if dex_nums[0] != "0":
        if len(dex_nums[0]) == 1:
            infobox.append("|ndex = 00" + dex_nums[0])
        elif len(dex_nums[0]) == 2:
            infobox.append("|ndex = 0" + dex_nums[0])
        else:
            infobox.append("|ndex = " + dex_nums[0])
    elif dex_nums[1] != "0":
        if len(dex_nums[1]) == 1:
            infobox.append("|ndex = X00" + dex_nums[1])
        elif len(dex_nums[1]) == 2:
            infobox.append("|ndex = X0" + dex_nums[1])
        else:
            infobox.append("|ndex = X" + dex_nums[1])
    else:
        if len(dex_nums[2]) == 1:
            infobox.append("|ndex = V00" + dex_nums[2])
        elif len(dex_nums[2]) == 2:
            infobox.append("|ndex = V0" + dex_nums[2])
        else:
            infobox.append("|ndex = V" + dex_nums[2])
    infobox.append("|image = " + pokemon_dict["Name"] + ".png")

    # Abilities
    reg_abilities = pokemon_dict["Abilities"].split(",")
    infobox.append("|ability1 = " + reg_abilities[0].title())
    if len(reg_abilities) > 1:
        infobox.append("|ability2 = " + reg_abilities[1].title())
    if "HiddenAbility" in pokemon_dict:
        infobox.append("|hiddenability = " +
                       pokemon_dict["HiddenAbility"].title())

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

    # Evs
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
    opening_paragraph = []

    dual_type = "dual-type" if "Type2" in pokemon_dict else ""
    typing = "{{Type|" + pokemon_dict["Type1"].title() + "}}/{{Type|" + pokemon_dict["Type2"].title(
    ) + "}}" if "Type2" in pokemon_dict else "{{Type|" + pokemon_dict["Type1"].title() + "}}"

    # First line
    opening_paragraph.append(
        f"'''{pokemon_dict['Name']}''' is a {dual_type} {typing}-type Pokémon.")

    # TODO: ADD EVOLUTIONS HERE

    return opening_paragraph


# Really no way to do this without knowing italian, just here for posterity
def create_pokedex_entry(pokemon_dict):
    pokedex_entry = []

    pokedex_entry.append("{{Dex")
    pokedex_entry.append("|type = " + pokemon_dict["Type1"].title())
    if "Type2" in pokemon_dict:
        pokedex_entry.append("|type2 = " + pokemon_dict["Type2"].title())
    pokedex_entry.append("''WIP''")
    pokedex_entry.append("}}")

    return pokedex_entry


def create_wild_items(pokemon_dict):
    wild_items = []

    # Open box & fix colouring
    wild_items.append("{{HeldItems")
    wild_items.append("|type = " + pokemon_dict["Type1"].title())
    if "Type2" in pokemon_dict:
        wild_items.append("|type2 = " + pokemon_dict["Type2"].title())

    # Add wild item data
    if "WildItemCommon" in pokemon_dict and "WildItemUncommon" in pokemon_dict and "WildItemRare" in pokemon_dict:
        if pokemon_dict["WildItemCommon"] == pokemon_dict["WildItemUncommon"] and pokemon_dict["WildItemUncommon"] == pokemon_dict["WildItemRare"]:
            item = item_info(pokemon_dict["WildItemCommon"].title())
            wild_items.append(
                "|always = {{Item|" + item + "}} [[" + item + "]]")
    else:
        if "WildItemCommon" in pokemon_dict:
            item = item_info(pokemon_dict["WildItemCommon"].title())
            wild_items.append(
                "|common = {{Item|" + item + "}} [[" + item + "]]")
        if "WildItemUncommon" in pokemon_dict:
            item = item_info(pokemon_dict["WildItemUncommon"].title())
            wild_items.append(
                "|uncommon = {{Item|" + item + "}} [[" + item + "]]")
        if "WildItemRare" in pokemon_dict:
            item = item_info(pokemon_dict["WildItemRare"].title())
            wild_items.append("|rare = {{Item|" + item + "}} [[" + item + "]]")

    # Close box
    wild_items.append("}}")

    return wild_items


def create_stats(pokemon_dict):
    stats = []

    stats.append("{{Stats")
    stats.append("|type = " + pokemon_dict["Type1"].title())
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
    type_effectiveness = []

    type_effectiveness.append("{{TypeEffectiveness")
    type_effectiveness.append("|type1 = " + pokemon_dict["Type1"].title())
    if "Type2" in pokemon_dict:
        type_effectiveness.append("|type2 = " + pokemon_dict["Type2"].title())
    type_effectiveness.append("}}")

    return type_effectiveness


def create_level_learnlist(pokemon_dict):
    level_learnlist = []

    second_type = pokemon_dict["Type2"].title(
    ) if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    level_learnlist.append("{{MoveLevelStart|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    moves = pokemon_dict["Moves"].split(",")
    for x in range(0, len(moves)-1, 2):
        move_stuff = move_info(moves[x+1].title()).split(",")
        # print(moves[x+1].title())

        if (move_stuff[1] == "yes") and (move_stuff[2] == pokemon_dict["Type1"].title() or move_stuff[2] == second_type):
            level_learnlist.append(
                "{{MoveLevel+|" + moves[x] + "|" + move_stuff[0] + "|'''}}")
        else:
            level_learnlist.append(
                "{{MoveLevel+|" + moves[x] + "|" + move_stuff[0] + "}}")

    level_learnlist.append("{{MoveLevelEnd|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    return level_learnlist


def create_tm_learnlist(pokemon_dict, tm_list):
    tm_learnlist = []

    second_type = pokemon_dict["Type2"].title(
    ) if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    tm_learnlist.append("{{MoveTMStart|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    for num in tm_list:
        tm_stuff = tm_info(num).split(",")
        if (tm_stuff[0] == "yes") and (tm_stuff[1] == pokemon_dict["Type1"].title() or tm_stuff[1] == second_type):
            tm_learnlist.append("{{MoveTM+|TM" + num + "|'''}}")
        else:
            tm_learnlist.append("{{MoveTM+|TM" + num + "}}")

    tm_learnlist.append("{{MoveTMEnd|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    return tm_learnlist


def create_breeding_learnlist(pokemon_dict):
    breeding_learnlist = []

    second_type = pokemon_dict["Type2"].title(
    ) if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    breeding_learnlist.append("{{MoveBreedStart|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    if "EggMoves" in pokemon_dict:
        egg_moves = pokemon_dict["EggMoves"].split(",")
        breeding_moves = []

        breed_string = "{{EM|107|Smeargle}} '''WIP'''" if "Field" in pokemon_dict[
            "Compatibility"] else "'''WIP'''"

        for move in egg_moves:
            # print(move.title())
            egg_stuff = move_info(move.title()).split(",")
            if (egg_stuff[1] == "yes") and (egg_stuff[2] == pokemon_dict["Type1"].title() or egg_stuff[2] == second_type):
                breeding_moves.append(
                    "{{MoveBreed+|" + breed_string + "|" + egg_stuff[0] + "|'''}}")
            else:
                breeding_moves.append(
                    "{{MoveBreed+|" + breed_string + "|" + egg_stuff[0] + "}}")

        for line in sorted(breeding_moves):
            breeding_learnlist.append(line)
    else:
        breeding_learnlist.append("{{MoveBreedNone}}")

    breeding_learnlist.append("{{MoveBreedEnd|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    return breeding_learnlist


def create_tutor_learnlist(pokemon_dict, tutor_list):
    tutor_learnlist = []

    second_type = pokemon_dict["Type2"].title(
    ) if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()

    tutor_learnlist.append("{{MoveTutorStart|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    tutor_moves = []
    for move in tutor_list:
        move_stuff = move_info(move).split(",")
        # print(move.title())
        if (move_stuff[1] == "yes") and (move_stuff[2] == pokemon_dict["Type1"].title() or move_stuff[2] == second_type):
            tutor_moves.append(
                "{{MoveTutor+|" + move_stuff[0] + "|'''|Varies}}")
        else:
            tutor_moves.append(
                "{{MoveTutor+|" + move_stuff[0] + "||Varies}}")

    for line in sorted(tutor_moves):
        tutor_learnlist.append(line)

    tutor_learnlist.append("{{MoveTutorEnd|" + pokemon_dict["Name"].title(
    ) + "|" + pokemon_dict["Type1"].title() + "|" + second_type + "}}")

    return tutor_learnlist


def create_sprites(pokemon_dict):

    second_type = pokemon_dict["Type2"].title(
    ) if "Type2" in pokemon_dict else pokemon_dict["Type1"].title()
    sprites = "{{sprites|name=" + pokemon_dict["Name"].title(
    ) + "|type=" + pokemon_dict["Type1"].title() + "|type2=" + second_type + "}}"

    return sprites
# endregion


def main():
    # Get the name of the Pokémon for the wiki page
    print()
    internal_name = input("Input the name of the pokemon: ")

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
    level_learnset = create_level_learnlist(pokemon_data)
    tm_learnset = create_tm_learnlist(pokemon_data, tm_data)
    egg_learnset = create_breeding_learnlist(pokemon_data)
    tutor_learnset = create_tutor_learnlist(pokemon_data, tutor_data)
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
    for line in level_learnset:
        wiki_page.append(str(line))

    wiki_page.append("==='''By TM/HM'''===")
    for line in tm_learnset:
        wiki_page.append(str(line))

    wiki_page.append("==='''By breeding'''===")
    for line in egg_learnset:
        wiki_page.append(str(line))

    wiki_page.append("==='''By tutoring'''===")
    for line in tutor_learnset:
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
