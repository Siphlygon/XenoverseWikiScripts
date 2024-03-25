# pylint: disable=locally-disabled, line-too-long, missing-module-docstring, too-few-public-methods
from data_access import static_encounters


# region Percentages
def calculate_percentages_and_secondary_info(biome_encounters, p_data, biome):
    """
    Branching method which decides the secondary information based on biome, and accesses other methods to calculate
    encounter percentages, which follow specific, positional rules based on the biome.

    The secondary information is returned as a string, and the percentage as an integer.

    :param list[str] biome_encounters: Encounter data for a particular biome.
    :param dict[str, str] p_data: A dictionary containing all the Pokémon's data in pokemon.txt.
    :param str biome: Biome type.
    :return tuple: Encounter percentage and any secondary information.
    """
    # Gets the positions of a Pokémon in a biome list
    indexes = [i + 1 for i, e in enumerate(biome_encounters) if p_data["InternalName"] in e]

    if biome in ["Land", "LandDay", "LandNight", "Cave"]:
        percentage = calculate_percentage_for_land_and_cave(indexes)
        if biome == "LandDay":
            secondary_info = "Day"
        elif biome == "Cave":
            secondary_info = "Cave"
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
    Calculate encounter percentages for land and cave biomes based on index in the list of encounters.

    Pokémon may appear at multiple indices, and the resultant encounter percentage is the sum. The percentage is decided
    as follows:

    Pokémon 1-2 - 20%
    Pokémon 3-6 - 10%
    Pokémon 7-8 - 5%
    Pokémon 9-10 - 4%
    Pokémon 11-12 - 1%

    :param list[int] indexes: Indexes of the Pokémon's encounter data.
    :return int: Calculated percentage of encounter.
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
    Calculate encounter percentages for rock smash and water biomes based on index in the list of encounters.

    Pokémon may appear at multiple indices, and the resultant encounter percentage is the sum. The percentage is decided
    as follows:

    Pokémon 1 - 60%
    Pokémon 2 - 30%
    Pokémon 3 - 5%
    Pokémon 4 - 4%
    Pokémon 5 - 1%

    :param list[int] indexes: Indexes of the Pokémon's encounter data.
    :return int: Calculated percentage of encounter.
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
    Calculate encounter percentages for old rod encounters based on index in the list of encounters.

    Pokémon may appear at multiple indices, and the resultant encounter percentage is the sum. The percentage is decided
    as follows:

    Pokémon 1 - 70%
    Pokémon 2 - 30%

    :param list[int] indexes: Indexes of the Pokémon's encounter data.
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
    Calculate encounter percentages for good rod encounters based on index in the list of encounters.

    Pokémon may appear at multiple indices, and the resultant encounter percentage is the sum. The percentage is decided
    as follows:

    Pokémon 1 - 60%
    Pokémon 2 - 20%
    Pokémon 3 - 20%

    :param list[int] indexes: Indexes of the Pokémon's encounter data.
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
    Calculate encounter percentages for super rod encounters based on index in the list of encounters.

    Pokémon may appear at multiple indices, and the resultant encounter percentage is the sum. The percentage is decided
    as follows:

    Pokémon 1 - 40%
    Pokémon 2 - 30%
    Pokémon 3 - 15%
    Pokémon 4 - 10%
    Pokémon 5 - 5%

    :param list[int] indexes: Indexes of the Pokémon's encounter data.
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
    Format the route string that will be displayed in the availability box, with the purpose to account for secondary
    information if present. The secondary information is displayed in parentheses after the location name.

    :param str loc_name: The name of the location.
    :param str secondary_info: Optional secondary information about the type of encounter.
    :return str: A formatted route string.
    """
    return f"[[{loc_name}]] ({secondary_info})" if secondary_info else f"[[{loc_name}]]"


def _process_location_data(loc, loc_name, p_data):
    """
    Process location data and access other methods to determine encounter percentages and secondary information.

    Breaks down the location data into biomes including the target Pokémon, and processes each biome separately. The
    resultant data is stored in a list of lists, with each sublist containing the percentage and route string for a
    particular biome.

    :param list[str] loc: Full encounter table for a particular location.
    :param str loc_name: Name of the location.
    :return list[list[str]]: Processed location data consisting of a percentage and a route string.
    """
    # Collection of location biomes, which is the type of encounter area
    location_biomes = ["Land", "LandDay", "LandNight", "Cave", "RockSmash", "Water", "OldRod", "GoodRod",
                       "SuperRod"]
    biome_dict = {}

    # Obtains the indexes where each different biome starts in a zone
    biome_indexes = [i for i, e in enumerate(loc) if e in location_biomes]

    # Not fully sure why, but the case of 1 biome in a location needs to be handled separately. Other fixes didn't work.
    if len(biome_indexes) == 1:
        biome_dict[loc[biome_indexes[0]]] = loc[biome_indexes[0] + 1:]
    else:
        # Adds the biomes as a key to a dictionary with the encounters in said biome as the value
        for n in range(0, len(biome_indexes) - 1):
            biome_dict[loc[biome_indexes[n]]] = loc[biome_indexes[n] + 1:biome_indexes[n + 1]]
        biome_dict[loc[biome_indexes[-1]]] = loc[biome_indexes[-1] + 1:]

    # Remove biomes without the Pokémon present
    biome_dict = {key: value for key, value in biome_dict.items() if p_data["InternalName"] in value}

    location_data = []
    for biome, data in biome_dict.items():
        percentages, secondary_info = calculate_percentages_and_secondary_info(data, p_data, biome)
        route_string = _format_route_string(loc_name, secondary_info)
        location_data.append([percentages, route_string])

    # If the Pokémon is present in multiple biomes in one location, blank secondary info
    if len(biome_dict) > 1:
        percentages = [p[0] for p in location_data]
        route_string = _format_route_string(loc_name, "")
        location_data = [[max(percentages), route_string]]

    return location_data


def _account_for_static_encounters(p_data, game_locations):
    """
    Accounts for an external list of static encounters.

    If the Pokémon is a static encounter, the information is added to the game locations list, indicating the location
    and type of static encounter, the latter if not a standard battle. The function also returns a boolean indicating if
    the Pokémon was a static encounter.

    :param dict[str, str] p_data: A dictionary containing all the Pokémon's data in pokemon.txt.
    :param list[str] game_locations: The wiki code to produce the availability information.
    :return bool: If the Pokémon was a static encounter.
    """
    static_enc = static_encounters(p_data["InternalName"])
    static_data = []
    if static_enc is not None:
        for route, static_type in static_enc.items():
            if static_type != "Static":
                static_data.append(f"[[{route}]] ({static_type})")
            else:
                static_data.append(f"[[{route}]]")
        game_locations.append("|one = " + ", ".join(static_data))
        return True
    return False


class LocationDataGenerator:
    """
    A class which extracts a Pokémon's data from encounters.txt, calculates the actual percentage of its appearance,
    and formats into a proper string.
    """
    def __init__(self, p_data, encounter_locs, loc_names):
        """
        The init function for LocationDataGenerator.

        :param dict[str, str] p_data: A dictionary containing all the Pokémon's data in pokemon.txt.
        :param list[str] encounter_locs: The encounter information for every location the Pokémon is present in.
        :param list[str] loc_names: The name of every location the Pokémon is available in.
        """
        self.p_data = p_data
        self.encounter_locs = encounter_locs
        self.loc_names = loc_names

    def create_game_locations(self):
        """
        Creates the wiki code to produce game locations for the Pokémon to be encountered given relevant information.

        Does not yet account for breeding only, or evolution only, which are sometimes the only way to obtain certain
        Pokémon.

        :return list[str]: The wiki code to produce the availability information.
        """
        game_locations = ["{{Availability", "|type = " + self.p_data["Type1"].title()]
        if "Type2" in self.p_data:
            game_locations.append("|type2 = " + self.p_data["Type2"].title())

        # If no wild encounters, the Pokémon is static only or evolution only or breeding only, not handled currently
        if not self.encounter_locs:
            if not _account_for_static_encounters(self.p_data, game_locations):
                game_locations.append("|none = WIP")
        else:
            _account_for_static_encounters(self.p_data, game_locations)

            enc_common = []
            enc_uncommon = []
            enc_rare = []

            # Stores the current number of the location being processed.
            curr_num = 0
            # There are no duplicate locations, ensured by data collection methods
            for loc in self.encounter_locs:
                location_data = _process_location_data(loc, self.loc_names[curr_num], self.p_data)
                for location in location_data:
                    if location[0] > 15:
                        enc_common.append(location[1])
                    elif location[0] > 5:
                        enc_uncommon.append(location[1])
                    else:
                        enc_rare.append(location[1])
                curr_num += 1

            if enc_common:
                game_locations.append("|common = " + ", ".join(enc_common))
            if enc_uncommon:
                game_locations.append("|uncommon = " + ", ".join(enc_uncommon))
            if enc_rare:
                game_locations.append("|rare = " + ", ".join(enc_rare))

        game_locations.append("}}")

        return game_locations
