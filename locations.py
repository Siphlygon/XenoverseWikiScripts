# pylint: disable=locally-disabled, line-too-long, missing-module-docstring, too-few-public-methods


# region Percentages
def calculate_percentages_and_secondary_info(data, pokemon_dict, biome):
    """
    Calculate encounter percentages and secondary information.

    :param list[str] data: Encounter data.
    :param dict[str, str] pokemon_dict: The full Pokémon information as a dictionary.
    :param str biome: Biome type.
    :return tuple: Percentages and secondary information.
    """
    indexes = [i for i, e in enumerate(data) if pokemon_dict["InternalName"] in e]
    if not indexes:
        return None, None

    if biome in ["Land", "LandDay", "LandNight", "Cave"]:
        percentage = calculate_percentage_for_land_and_cave(indexes)
        if biome == "LandDay":
            secondary_info = "Day"
        else:
            secondary_info = "Night" if biome == "LandNight" else ""

    elif biome in ["RockSmash", "Water"]:
        percentage = calculate_percentage_for_rock_smash_and_water(indexes)
        secondary_info = "Rock Smash" if biome == "RockSmash" else "Surf"

    elif biome == "OldRod":
        percentage = calculate_percentage_for_old_rod(indexes)
        secondary_info = "Old Rod"

    elif biome == "GoodRod":
        percentage = calculate_percentage_for_good_rod(indexes)
        secondary_info = "Good Rod"

    else:  # SuperRod
        percentage = calculate_percentage_for_super_rod(indexes)
        secondary_info = "Super Rod"

    return percentage, secondary_info


def calculate_percentage_for_land_and_cave(indexes):
    """
    Calculate percentage for land and cave biomes.

    :param list[int] indexes: Indexes of encounter data.
    :return int: Calculated percentage.
    """
    percentage = 0
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
    return percentage


def calculate_percentage_for_rock_smash_and_water(indexes):
    """
    Calculate percentage for rock smash and water biomes.

    :param list[int] indexes: Indexes of encounter data.
    :return int: Calculated percentage.
    """
    percentage = 0
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
    return percentage


def calculate_percentage_for_old_rod(indexes):
    """
    Calculate percentage for Old Rod encounters.

    :param list[int] indexes: Indexes of encounter data.
    :return int: Calculated percentage.
    """
    percentage = 0
    for index in indexes:
        if index in [1]:
            percentage += 70
        else:
            percentage += 30
    return percentage


def calculate_percentage_for_good_rod(indexes):
    """
    Calculate percentage for Good Rod encounters.

    :param list[int] indexes: Indexes of encounter data.
    :return int: Calculated percentage.
    """
    percentage = 0
    for index in indexes:
        if index in [1]:
            percentage += 60
        else:
            percentage += 20
    return percentage


def calculate_percentage_for_super_rod(indexes):
    """
    Calculate percentage for Super Rod encounters.

    :param list[int] indexes: Indexes of encounter data.
    :return int: Calculated percentage.
    """
    percentage = 0
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
    return percentage
# endregion


def _format_route_string(loc_name, secondary_info):
    """
    Format route string.

    :param str loc_name: Location name.
    :param str secondary_info: Secondary information.
    :return str: Formatted route string.
    """
    return f"[[{loc_name}]] ({secondary_info})" if secondary_info else f"[[{loc_name}]]"


def _process_location_data(loc, location_biomes, loc_name, p_data):
    """
    Process location data to determine encounter percentages and secondary information.

    :param list[str] loc: Encounter information for a location.
    :param list[str] location_biomes: Collection of location biomes.
    :param str loc_name: Name of the location.
    :return dict: Processed location data.
    """
    loc_dict = {}
    biome_indexes = [i for i, e in enumerate(loc) if e in location_biomes]

    if len(biome_indexes) == 1:
        loc_dict[loc[biome_indexes[0]]] = loc[biome_indexes[0] + 1:]
    else:
        for n in range(0, len(biome_indexes) - 1, 2):
            loc_dict[loc[biome_indexes[n]]] = loc[biome_indexes[n] + 1:biome_indexes[n + 1]]

    location_data = {}
    for biome, data in loc_dict.items():
        percentages, secondary_info = calculate_percentages_and_secondary_info(data, p_data, biome)
        if percentages:
            route_string = _format_route_string(loc_name, secondary_info)
            location_data[biome] = (percentages, route_string)

    return location_data


def _update_encounter_lists(enc_common, enc_uncommon, enc_rare, location_data):
    """
    Update encounter lists.

    :param list[str] enc_common: List of common encounters.
    :param list[str] enc_uncommon: List of uncommon encounters.
    :param list[str] enc_rare: List of rare encounters.
    :param dict location_data: Processed location data.
    """
    for biome, (percentage, route_string) in location_data.items():
        if percentage > 15:
            enc_common.append(route_string)
        elif percentage > 5:
            enc_uncommon.append(route_string)
        else:
            enc_rare.append(route_string)


def _append_encounter_lists_to_game_locations(game_locations, enc_common, enc_uncommon, enc_rare):
    """
    Append encounter lists to game locations.

    :param list[str] game_locations: List of game locations.
    :param list[str] enc_common: List of common encounters.
    :param list[str] enc_uncommon: List of uncommon encounters.
    :param list[str] enc_rare: List of rare encounters.
    """
    if enc_common:
        game_locations.append("|common = " + ", ".join(enc_common))
    if enc_uncommon:
        game_locations.append("|uncommon = " + ", ".join(enc_uncommon))
    if enc_rare:
        game_locations.append("|rare = " + ", ".join(enc_rare))


class LocationDataGenerator:
    """
    A class which extracts a Pokémon's data from encounters.txt, calculates the actual percentage of its appearance,
    and formats into a proper string.
    """
    def __init__(self, p_data, loc_encounters, loc_names):
        """
        The init function for LocationDataGenerator.

        :param dict[str, str] p_data: A dictionary containing all the Pokémon's data in pokemon.txt.
        :param list[str] loc_encounters: The encounter information for every relevant location.
        :param list[str] loc_names: The name of every location the Pokémon is available in.
        """
        self.p_data = p_data
        self.loc_encounters = loc_encounters
        self.loc_names = loc_names

    def create_game_locations(self):
        """
        Creates the game locations for the Pokémon to be encountered given relevant information. Does not yet account for
        static encounters, breeding only, or evolution only.

        :return list[str]: The wiki code to produce the availability information.
        """
        # Collection of location biomes, which is the type of encounter area
        location_biomes = ["Land", "LandDay", "LandNight", "Cave", "RockSmash", "Water", "OldRod", "GoodRod",
                           "SuperRod"]

        # Start game location box
        game_locations = ["{{Availability", "|type = " + self.p_data["Type1"].title()]
        if "Type2" in self.p_data:
            game_locations.append("|type2 = " + self.p_data["Type2"].title())

        # If no wild encounters, the Pokémon is static only or evolution only or breeding only
        if not self.loc_encounters:
            game_locations.append("|none = WIP")
        else:
            # Initialises lists to hold encounter information for the three different rarities
            enc_common = []
            enc_uncommon = []
            enc_rare = []

            # Stores the current number of the location being processed.
            curr_num = 0

            for loc in self.loc_encounters:
                location_data = _process_location_data(loc, location_biomes, self.loc_names[curr_num], self.p_data)
                _update_encounter_lists(enc_common, enc_uncommon, enc_rare, location_data)
                curr_num += 1

            _append_encounter_lists_to_game_locations(game_locations, enc_common, enc_uncommon, enc_rare)

        game_locations.append("}}")

        return game_locations
