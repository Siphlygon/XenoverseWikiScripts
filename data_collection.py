# pylint: disable=locally-disabled, line-too-long, missing-module-docstring

from data_access import location_info


def read_file_lines(filename):
    """
    Read lines from a file and return them as a list.

    :param str filename: The name of the file to read.
    :return list: The list of lines read from the file.
    """
    with open(filename, encoding="utf8") as file:
        return [line.rstrip() for line in file.readlines()]


def find_location_indices(idx, line_list):
    """
    Find the start and end indices of a location's encounter data.

    :param int idx: The index of the line containing the Pokémon's mention.
    :param list line_list: The list of lines in encounters.txt.
    :return tuple: The start and end indices of the location's encounter data.
    """
    start, end = 0, 0
    for a in range(idx, 0, -1):
        start = a
        if line_list[a] == "#########################":
            break
    for b in range(idx + 1, len(line_list), 1):
        end = b
        if line_list[b] == "#########################":
            break
    return start, end


class DataCollection:
    """
    A class that contains methods to extract all related information to a Pokémon from the game's data files.
    """

    def __init__(self, name):
        """
        The init function of DataCollection.

        :param str name: The internal name of a Pokémon.
        """
        self.name = name
        self.pokemon_path = "gamedata/pokemon.txt"
        self.tm_path = "gamedata/tm.txt"
        self.encounters_path = "gamedata/encounters.txt"

    def extract_pokemon_data(self):
        """
        Extract and return all information for a Pokémon from a given file.

        :return dict[str, str]: A dictionary containing all relevant information found in the file for the Pokémon.
        """
        line_list = read_file_lines(self.pokemon_path)
        raw_data = []
        found_pokemon = False

        for idx, line in enumerate(line_list):
            if line == "InternalName=" + self.name:
                found_pokemon = True
                raw_data = line_list[idx - 1:idx + 1]
                continue

            if found_pokemon:
                raw_data.append(line)

                # Indicates the start of the next Pokémon's data - stop here
                if "InternalName" in line:
                    # Size of Pokémon sections are not constant, but the next InternalName is always 3 lines too far.
                    raw_data.remove(line)
                    raw_data.remove(line_list[idx - 1])
                    raw_data.remove(line_list[idx - 2])
                    break

        return {key: value for line in raw_data for key, value in [line.split('=', 1)]}

    def extract_move_data(self):
        """
        Extract and return all TM or tutor move information for a Pokémon from a given file.

        :return tuple[list[str], list[str]]: The list of moves learnable by the Pokémon from the file.
        """
        line_list = read_file_lines(self.tm_path)

        tm_list = []
        tutor_list = []

        for idx, line in enumerate(line_list):
            names = line.split(",")

            # Because X or other form pokemon also will contain the same name (e.g.: SHYLEONX has SHYLEON in it),
            # this ensures only exact matches to the given internal name are selected
            matches = set(names).intersection({self.name})

            # All moves up to line 194 are TM moves, everything else are tutor moves
            if len(matches) > 0:
                if idx < 194:
                    tm_list.append(line_list[idx - 1].strip("[]"))
                else:
                    tutor_list.append(line_list[idx - 1].strip("[]"))

        return tm_list, tutor_list

    def extract_encounter_data(self):
        """
        Extract and return all encounter information for a Pokémon from encounters.txt.

        :return tuple: The encounter tables for all relevant locations and the list of zones for those locations.
        """
        line_list = read_file_lines(self.encounters_path)

        encounter_info = []
        found_locations = []

        for idx, line in enumerate(line_list):
            if self.name in line:
                start, end = find_location_indices(idx, line_list)

                # Finds the zone ID, which any one location can have multiple of
                zone_id = line_list[start + 1].split("#")[0].rstrip()

                # Ensures that locations aren't processed multiple times due to different zones
                if location_info(zone_id) not in found_locations:
                    found_locations.append(location_info(zone_id))

                    # Remove level number, unnecessary for this program
                    zone_encounters = line_list[start:end]
                    formatted_encounters = [''.join(x for x in i if x.isalpha()) for i in zone_encounters]

                    encounter_info.append(formatted_encounters)

        return encounter_info, found_locations
