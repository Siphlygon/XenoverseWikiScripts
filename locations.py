# pylint: disable=locally-disabled, line-too-long, missing-module-docstring, too-few-public-methods


# region Percentages
def calculate_percentages_and_secondary_info(biome_encounters, p_data, biome):
    """
    Calculate encounter percentages and secondary information for a Pokémon in a given biome.

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

    :param list[int] indexes: Indexes of the Pokémon's encounter data.
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
    Calculate encounter percentages for rock smash and water biomes based on index in the list of encounters.

    :param list[int] indexes: Indexes of the Pokémon's encounter data.
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
    Calculate encounter percentages for old rod encounters based on index in the list of encounters.

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
    Format the route string that will be displayed in the availability box.

    :param str loc_name: The name of the location.
    :param str secondary_info: Optional secondary information about the type of encounter.
    :return str: A formatted route string.
    """
    return f"[[{loc_name}]] ({secondary_info})" if secondary_info else f"[[{loc_name}]]"


def _process_location_data(loc, loc_name, p_data):
    """
    Process location data to determine encounter percentages and secondary information.

    :param list[str] loc: Encounter information for a location.
    :param str loc_name: Name of the location.
    :return dict: Processed location data.
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
        Creates the game locations for the Pokémon to be encountered given relevant information. Does not yet account
        for static encounters, breeding only, or evolution only.

        :return list[str]: The wiki code to produce the availability information.
        """
        game_locations = ["{{Availability", "|type = " + self.p_data["Type1"].title()]
        if "Type2" in self.p_data:
            game_locations.append("|type2 = " + self.p_data["Type2"].title())

        # If no wild encounters, the Pokémon is static only or evolution only or breeding only, not handled currently
        if not self.encounter_locs:
            game_locations.append("|none = WIP")
        else:
            enc_common = []
            enc_uncommon = []
            enc_rare = []

            # Stores the current number of the location being processed.
            curr_num = 0

            # There are no duplicate locations, ensured by data collection methods
            for loc in self.encounter_locs:
                location_data = _process_location_data(loc, self.loc_names[curr_num], self.p_data)
                print(location_data)
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
