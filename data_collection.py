# pylint: disable=locally-disabled, line-too-long, missing-module-docstring
import logging


def read_file_lines(filename):
    """
    Read lines from a file and return them as a list, stripping any trailing whitespaces. Reduces the time a file is
    open, as it is closed automatically after the function is done.

    :param str filename: The name of the file to read.
    :return list: The list of lines read from the file.
    """
    with open(filename, encoding="utf8") as file:
        return [line.rstrip() for line in file.readlines()]


def find_location_indices(idx, line_list):
    """
    Find the start and end indices of a location's encounter data.

    We first instead find the index, idx, of a specific Pokémon's mention in said location. We then iterate backwards
    and forwards from that index to find the start and end of the location's encounter data by searching for hashes.

    :param int idx: The index of the line containing the Pokémon's mention.
    :param list line_list: The list of lines in encounters.txt.
    :return tuple: The start and end indices of the location's encounter data.
    """
    start, end = 0, 0
    for a in range(idx, 0, -1):
        start = a
        if "#" in line_list[a]:
            break
    for b in range(idx + 1, len(line_list), 1):
        end = b
        if "#" in line_list[b]:
            break
    return start, end


class DataCollection:
    """
    A class that contains methods to extract all related information to a Pokémon from the game's data files.
    """

    def __init__(self, name, pokemon_path="gamedata/pokemon.txt", tm_path="gamedata/tm.txt", encounters_path="gamedata/encounters.txt"):
        """
        The init function of DataCollection.

        :param str name: The internal name of a Pokémon.
        :param str pokemon_path: The path to the file containing Pokémon data.
        :param str tm_path: The path to the file containing TM and tutor move data.
        :param str encounters_path: The path to the file containing encounter data.
        """
        self.name = name
        self.pokemon_path = pokemon_path
        self.tm_path = tm_path
        self.encounters_path = encounters_path
        self.logger = logging.getLogger(__name__)

    def extract_pokemon_data(self):
        """
        Extract and return all information for a Pokémon from pokemon.txt.

        This includes the Pokémon's name, type, base stats, and other relevant information. The data is stored in a
        dictionary, with the type of data as the key (e.g., "Name", "Type1", "Type2", "BaseStats", etc.), and the actual
        data as the value.

        :return dict[str, str]: A dictionary containing all relevant information found in the file for the Pokémon.
        """
        line_list = read_file_lines(self.pokemon_path)
        raw_data = []
        found_pokemon = False

        for idx, line in enumerate(line_list):
            if line == "InternalName=" + self.name:
                found_pokemon = True
                raw_data = line_list[idx - 2:idx + 1]
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

        try:
            raw_data[0] = "InternalNumber=" + raw_data[0].replace("[", "").replace("]", "")
        except IndexError as exc:
            self.logger.error("Could not find internal name '%s' in the file.", self.name)
            raise ValueError(f"Could not find internal name '{self.name}' in the file.") from exc

        return {key: value for line in raw_data for key, value in [line.split('=', 1)]}

    def extract_move_data(self):
        """
        Extract and return all TM or tutor move information for a Pokémon from tm.txt.

        The separation between the two types of moves is not obviously indicated within the file itself, and so the
        program must determine this manually. The data is stored in a tuple, with the first element being the list of TM
        moves, and the second being the list of tutor moves.

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

        This is stored in numbered zones in the game's data, and any one individual location may have multiple different
        zones and different encounter tables. The data is stored in a list of lists, with each list containing the
        encounter tables for a specific location. The list of locations processed is also returned.

        :return tuple[list[list[str]], list[str]]: The encounter tables for relevant locations and the locations processed.
        """
        line_list = read_file_lines(self.encounters_path)

        encounter_info = []
        found_zones = []

        for idx, line in enumerate(line_list):
            if self.name in line:
                start, end = find_location_indices(idx, line_list)

                # Finds the zone ID, which any one location can have multiple of
                zone_id = line_list[start].split("#")[0].rstrip()

                # Ensures that zones aren't processed multiple times
                if zone_id not in found_zones:
                    found_zones.append(zone_id)

                    # Remove level number, unnecessary for this program
                    zone_encounters = line_list[start:end]

                    # Strip numbers from everything and ignore first two lines; unnecessary now
                    formatted_encounters = [''.join(x for x in i if x.isalpha()) for i in zone_encounters[2:]]
                    encounter_info.append(formatted_encounters)

        return encounter_info, found_zones
