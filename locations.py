# pylint: disable=locally-disabled, line-too-long, missing-module-docstring, too-few-public-methods
from data_access import location_info, static_encounters, location_order
from utility_methods import get_two_types


# region Percentages
def calculate_rarity_and_secondary_info(biome_encounters, p_data, biome):
    """
    Branching method which decides the secondary information based on biome, and accesses other methods to calculate
    encounter rarity, which follow specific, positional rules based on the biome.

    The secondary information is returned as a string, and the rarity as a string.

    :param list[str] biome_encounters: Encounter data for a particular biome.
    :param dict[str, str] p_data: A dictionary containing all the Pokémon's data in pokemon.txt.
    :param str biome: Biome type.
    :return tuple: Encounter rarity and any secondary information.
    """
    # Gets the positions of a Pokémon in a biome list
    indexes = [i + 1 for i, e in enumerate(biome_encounters) if p_data["InternalName"] in e]

    if biome in ["Land", "LandDay", "LandNight", "Cave"]:
        rarity = calculate_rarity_for_land_and_cave(indexes)
        if biome == "LandDay":
            secondary_info = "Day"
        elif biome == "Cave":
            secondary_info = "Cave"
        else:
            secondary_info = "Night" if biome == "LandNight" else ""

    elif biome in ["RockSmash", "Water"]:
        rarity = calculate_rarity_for_rock_smash_and_water(indexes)
        secondary_info = "Rock Smash" if biome == "RockSmash" else "Surfing"

    elif biome == "OldRod":
        rarity = calculate_rarity_for_old_rod(indexes)
        secondary_info = "Old Rod"

    elif biome == "GoodRod":
        rarity = calculate_rarity_for_good_rod(indexes)
        secondary_info = "Good Rod"

    else:  # SuperRod
        rarity = calculate_rarity_for_super_rod(indexes)
        secondary_info = "Super Rod"

    return rarity, secondary_info


def calculate_rarity_for_land_and_cave(indexes):
    """
    Calculate encounter percentages and thus rarity for land and cave biomes based on index in the list of encounters.

    Pokémon may appear at multiple indices, and the resultant encounter percentage is the sum. The percentage is decided
    as follows:

    Pokémon 1-2 - 20%
    Pokémon 3-6 - 10%
    Pokémon 7-8 - 5%
    Pokémon 9-10 - 4%
    Pokémon 11-12 - 1%

    For this specific biome, common rarity is >=20%, uncommon rarity is >5%, and rare rarity is <=5%.

    :param list[int] indexes: Indexes of the Pokémon's encounter data.
    :return string: Calculated rarity of encounter.
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

    if percentage >= 20:
        rarity = "Common"
    elif percentage > 5:
        rarity = "Uncommon"
    else:
        rarity = "Rare"

    return rarity


def calculate_rarity_for_rock_smash_and_water(indexes):
    """
    Calculate encounter percentages and thus rarity for rock smash and water biomes based on index in the list of
    encounters.

    Pokémon may appear at multiple indices, and the resultant encounter percentage is the sum. The percentage is decided
    as follows:

    Pokémon 1 - 60%
    Pokémon 2 - 30%
    Pokémon 3 - 5%
    Pokémon 4 - 4%
    Pokémon 5 - 1%

    For this specific biome, common rarity is >=40%, uncommon rarity is >10%, and rare rarity is <=10%.

    :param list[int] indexes: Indexes of the Pokémon's encounter data.
    :return string: Calculated rarity of encounter.
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

    if percentage >= 40:
        rarity = "Common"
    elif percentage > 10:
        rarity = "Uncommon"
    else:
        rarity = "Rare"

    return rarity


def calculate_rarity_for_old_rod(indexes):
    """
    Calculate encounter percentages and thus rarity for old rod encounters based on index in the list of encounters.

    Pokémon may appear at multiple indices, and the resultant encounter percentage is the sum. The percentage is decided
    as follows:

    Pokémon 1 - 70%
    Pokémon 2 - 30%

    For this specific biome, common rarity is >=70%, and uncommon rarity is <=30%.

    :param list[int] indexes: Indexes of the Pokémon's encounter data.
    :return string: Calculated rarity.
    """
    percentage = 0
    for index in indexes:
        if index in [1]:
            percentage += 70
        else:
            percentage += 30

    if percentage >= 70:
        rarity = "Common"
    else:
        rarity = "Uncommon"

    return rarity


def calculate_rarity_for_good_rod(indexes):
    """
    Calculate encounter percentages and thus rarity for good rod encounters based on index in the list of encounters.

    Pokémon may appear at multiple indices, and the resultant encounter percentage is the sum. The percentage is decided
    as follows:

    Pokémon 1 - 60%
    Pokémon 2 - 20%
    Pokémon 3 - 20%

    For this specific biome, common rarity is >=40%, uncommon rarity is <40%,

    :param list[int] indexes: Indexes of the Pokémon's encounter data.
    :return string: Calculated rarity.
    """
    percentage = 0
    for index in indexes:
        if index in [1]:
            percentage += 60
        else:
            percentage += 20

    if percentage >= 40:
        rarity = "Common"
    else:
        rarity = "Uncommon"

    return rarity


def calculate_rarity_for_super_rod(indexes):
    """
    Calculate encounter percentages and thus rarity for super rod encounters based on index in the list of encounters.

    Pokémon may appear at multiple indices, and the resultant encounter percentage is the sum. The percentage is decided
    as follows:

    Pokémon 1 - 40%
    Pokémon 2 - 30%
    Pokémon 3 - 15%
    Pokémon 4 - 10%
    Pokémon 5 - 5%

    For this specific biome, common rarity is >=30%, uncommon rarity is >10%, and rare rarity is <=10%.

    :param list[int] indexes: Indexes of the Pokémon's encounter data.
    :return string: Calculated rarity.
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

    if percentage >= 30:
        rarity = "Common"
    elif percentage > 10:
        rarity = "Uncommon"
    else:
        rarity = "Rare"

    return rarity
# endregion


def _process_zone_biomes(zone, loc_name, p_data):
    """
    Breaks down zone data into biomes and determines encounter percentages and secondary information.

    Breaks down the zone data into biomes which include the target Pokémon, and processes each biome separately. The
    resultant data is stored in a list of lists, with each sublist containing the rarity and route string for a
    particular biome.

    :param list[str] zone: Full encounter table for a particular zone.
    :param str loc_name: Name of the location.
    :return list[list[str]]: Processed zone data consisting of a rarity, route name, and secondary information.
    """
    # Collection of location biomes, which is the type of encounter area
    location_biomes = ["Land", "LandDay", "LandNight", "Cave", "RockSmash", "Water", "OldRod", "GoodRod", "SuperRod"]
    biome_dict = {}

    # Obtains the indexes where each different biome starts in a zone
    biome_indexes = [i for i, e in enumerate(zone) if e in location_biomes]

    # Not fully sure why, but the case of 1 biome in a location needs to be handled separately. Other fixes didn't work.
    if len(biome_indexes) == 1:
        biome_dict[zone[biome_indexes[0]]] = zone[biome_indexes[0] + 1:]
    else:
        # Adds the biomes as a key to a dictionary with the encounters in said biome as the value
        for n in range(0, len(biome_indexes) - 1):
            biome_dict[zone[biome_indexes[n]]] = zone[biome_indexes[n] + 1:biome_indexes[n + 1]]
        biome_dict[zone[biome_indexes[-1]]] = zone[biome_indexes[-1] + 1:]

    # Remove biomes without the Pokémon present
    biome_dict = {key: value for key, value in biome_dict.items() if p_data["InternalName"] in value}

    zone_data = []
    biomes_processed = {}
    for idx, (biome, data) in enumerate(biome_dict.items()):
        biomes_processed[biome] = idx

        rarity, secondary_info = calculate_rarity_and_secondary_info(data, p_data, biome)
        zone_data.append([rarity, (loc_name, secondary_info)])

    # Can't believe I have to account for this, but old "Land" code is overwritten by "LandDay" and "LandNight"
    if biomes_processed.keys() == {"Land", "LandDay", "LandNight"}:
        del zone_data[biomes_processed["Land"]]

    return zone_data


def _add_rarity_lists(location_data, game_locations):
    """
    Add rarity lists to the game locations list.

    The location data is split into three lists based on rarity, and then formatted into locations grouped by secondary
    information. The rarity lists are then added to the game locations list.

    :param dict[tuple[str, str], str]: The merged location data to be rarity analysed.
    :param list[str] game_locations: The wiki code to produce the availability information.
    """
    enc_common = []
    enc_uncommon = []
    enc_rare = []

    # Add the location data to the appropriate rarity list
    for location in location_data:
        if location[0] == "Common":
            enc_common.append([location[1][0], location[1][1]])
        elif location[0] == "Uncommon":
            enc_uncommon.append([location[1][0], location[1][1]])
        else:
            enc_rare.append([location[1][0], location[1][1]])

    rarity_lists = {"common": enc_common, "uncommon": enc_uncommon, "rare": enc_rare}

    # Format the rarity lists into display
    for rarity, rarity_list in rarity_lists.items():
        if rarity_list:
            _merge_day_and_night(rarity_list)
            rarity_list = _format_rarity_list(rarity_list)

            # Specifically setup as to facilitate line break between sections
            rarity_string = f"|{rarity} = "
            for i in range(0, len(rarity_list), 2):
                rarity_string += ", ".join(rarity_list[i])

                # Make sure line doesn't end on a <hr>
                if i + 1 < len(rarity_list) - 1:
                    rarity_string += rarity_list[i + 1]
                else:
                    rarity_string += rarity_list[i + 1].replace("<hr>", "")
            game_locations.append(rarity_string)


def _format_rarity_list(rarity_list):
    """
    Format the rarity list into separate sections based on secondary information.

    The rarity list is split into sections based on the secondary information, which are delimited by line breaks <br>.
    Secondary information outside normal encounters is enclosed in parentheses.

    :param list[list[str]] rarity_list: The list of routes & secondary information for a particular rarity.
    :return list[str]: The formatted rarity list.
    """
    encounter_types = {
        "": "Normal",
        "Day": "Normal",
        "Night": "Normal",
        "Day Only": "Normal",
        "Night Only": "Normal",
        "Cave": "Normal",
        "Rock Smash": "Rock Smash",
        "Surfing": "Surfing",
        "Old Rod": "Old Rod",
        "Good Rod": "Good Rod",
        "Super Rod": "Super Rod"
    }

    # Create a map of rarity to encounter lists
    rarity_map = {encounter_type: [] for encounter_type in encounter_types.values()}

    # Populate the map with the encounters with appropriate encounters
    for encounter in rarity_list:
        if encounter[1] in ["Day", "Night", "Day Only", "Night Only"]:
            rarity_map[encounter_types.get(encounter[1])].append("[[" + encounter[0] + "]] (" + encounter[1] + ")")
        else:
            rarity_map[encounter_types.get(encounter[1])].append("[[" + encounter[0] + "]]")

    new_rarity_list = []
    for encounter_type, biome in rarity_map.items():
        if biome:
            new_rarity_list.append(biome)
            if encounter_type != "Normal":
                new_rarity_list.append(f" ({encounter_type})<hr> ")
            else:
                new_rarity_list.append(" <hr> ")

    return new_rarity_list


def _merge_same_location_data(all_zone_data):
    """
    Merge different zone datas for the same location.

    Any location may have multiple zones, and although many have duplicate encounter tables, not all do. This function
    merges the data for the same location, keeping only the highest encounter rarity for display purposes. A dictionary
    is used to weight the rarity of the encounters such that the most common rarity is displayed.

    :param  list[list[str | tuple[str, str]]] all_zone_data: The list of all zone data.
    :return dict[tuple[str, str], str]: The merged location data.
    """
    location_data = {}
    rarity_weight = {"Common": 3, "Uncommon": 2, "Rare": 1}
    for zone in all_zone_data:
        if zone[1] in location_data:
            if rarity_weight[zone[0]] > rarity_weight[location_data[zone[1]]]:
                location_data[zone[1]] = zone[0]
        else:
            location_data[zone[1]] = zone[0]

    return location_data


def _specify_day_night_exclusivity(location_dict):
    """
    Specify if a location is day or night exclusive.

    If a location only has data for Day or Night, the function will modify the location data to reflect this. This is
    to differentiate between encounters which are e.g., Day exclusive (Day Only) and those which can have different
    encounter chances and thus rarity in Day and Night.

    :param dict[tuple[str, str], str] location_dict: The merged location data.
    :return dict[tuple[str, str], str]: The modified location data.
    """
    modified_location_dict = {}
    for (route, secondary_info), rarity in location_dict.items():
        if secondary_info == "Day" and (route, "Night") not in location_dict:
            modified_location_dict[(route, "Day Only")] = rarity
        elif secondary_info == "Night" and (route, "Day") not in location_dict:
            modified_location_dict[(route, "Night Only")] = rarity
        else:
            modified_location_dict[(route, secondary_info)] = rarity

    return modified_location_dict


def _merge_day_and_night(rarity_list):
    """
    Merge same-rarity (implicit) encounters on the same route if they are consecutively day and night.

    :param list[list[str]] rarity_list: The list of routes & secondary information for a particular rarity.
    """
    n = 1
    day_night = ["Day", "Night"]
    while n < len(rarity_list):
        old_rte = rarity_list[n - 1][0]
        rte = rarity_list[n][0]
        old_bio = rarity_list[n - 1][1]
        bio = rarity_list[n][1]
        if old_rte == rte and ([old_bio, bio] == day_night or (old_bio == "" and bio in [day_night, "Day Only", "Night Only"])):
            rarity_list[n - 1][1] = ""
            del rarity_list[n]
        else:
            n += 1


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
    def __init__(self, p_data, encounter_locs, zone_ids):
        """
        The init function for LocationDataGenerator.

        :param dict[str, str] p_data: A dictionary containing all the Pokémon's data in pokemon.txt.
        :param list[list[str]] encounter_locs: The encounter information for every location the Pokémon is present in.
        :param list[str] zone_ids: The ID of every zone the Pokémon is available in.
        """
        self.p_data = p_data
        self.first_type, self.second_type = get_two_types(p_data)
        self.encounter_locs = encounter_locs
        self.zone_ids = zone_ids

    def create_game_locations(self):
        """
        Creates the wiki code to produce game locations for the Pokémon to be encountered given relevant information.

        Does not yet account for breeding only, or evolution only, which are sometimes the only way to obtain certain
        Pokémon.

        :return list[str]: The wiki code to produce the availability information.
        """
        game_locations = ["{{Availability", f"|type = {self.first_type}"]
        if self.first_type != self.second_type:
            game_locations.append(f"|type2 = {self.second_type}")

        # If no wild encounters, the Pokémon is static only or evolution only or breeding only, not handled currently
        if not self.encounter_locs:
            if not _account_for_static_encounters(self.p_data, game_locations):
                game_locations.append("|none = WIP")
        else:
            _account_for_static_encounters(self.p_data, game_locations)

            # Process the encounter data for each zone
            all_zone_data = []
            for idx, zone in enumerate(self.encounter_locs):
                loc_name = location_info(self.zone_ids[idx])
                zone_data = _process_zone_biomes(zone, loc_name, self.p_data)
                all_zone_data.extend(zone_data)

            # Sort based on an order loosely connected to in game order
            sorting_order = location_order()
            all_zone_data.sort(key=lambda x: (sorting_order[x[1][0]], x[1][1]))

            # Multiple zones are present in the same location, with different encounter tables. Only display the highest
            location_dict = _merge_same_location_data(all_zone_data)
            modified_location_dict = _specify_day_night_exclusivity(location_dict)
            location_data = [[v, k] for k, v in modified_location_dict.items()]

            _add_rarity_lists(location_data, game_locations)

        game_locations.append("}}")

        return game_locations
