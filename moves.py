# pylint: disable=too-many-lines, line-too-long, missing-module-docstring, import-error, too-many-arguments
from data_access import (pokemon_info, move_info, tm_info)
from utility_methods import find_dex_number, get_two_types
from evolution import EvolutionHandler
from data_collection import DataCollection


def _is_stab(move_data, type1, type2):
    """
    Decides if a move will gain a Same Type Attack Bonus (STAB) when used by the Pokémon. This occurs if the move's type
    is the same as one of the Pokémon's.

    :param list[str] move_data: The data relating to the move being considered, as in move_info.json.
    :param str type1: The first type of the Pokémon.
    :param str type2: The second type of the Pokémon, which may be the same as type1 if single-typed.
    :return bool: If the move will gain STAB when used.
    """
    return move_data["STAB"] == "yes" and (move_data["Type"] == type1 or move_data["Type"] == type2)


def _add_level_moves_to_list(moves, type1, type2, future_type, list_name):
    """
    Adds moves a Pokémon learns by level up to a given list in wiki format, accounting for STAB and indicating level.

    Moves are added in pairs, with the first element being the level and the second being the move learned.

    :param list[str] moves: A list of levels and moves learned at those levels in sequential order.
    :param str type1: The first type of the Pokémon.
    :param str type2: The second type of the Pokémon, which may be the same as type1 if single-typed.
    :param str future_type: The type of the Pokémon at the next evolution stage.
    :param list[str] list_name: The wiki template to add formatted moves to.
    """
    for x in range(0, len(moves) - 1, 2):
        move_data = move_info(moves[x + 1])

        if _is_stab(move_data, type1, type2):
            list_name.append("{{MoveLevel+|" + moves[x] + "|" + move_data["Name"] + "|'''}}")
        elif _is_stab(move_data, future_type, future_type):
            list_name.append("{{MoveLevel+|" + moves[x] + "|" + move_data["Name"] + "|''}}")
        else:
            list_name.append("{{MoveLevel+|" + moves[x] + "|" + move_data["Name"] + "}}")


def _add_tm_moves_to_list(moves, type1, type2, future_type, list_name):
    """
    Adds moves a Pokémon learns by TM to a given list in wiki format, accounting for STAB and indicating TM number.

    TMs are stored as move names in tm.txt, but are converted to TM numbers (01-95) for the wiki, which is what the
    reference dictionary is used for.

    :param list[str] moves: A list of TM moves learnable by a Pokémon.
    :param str type1: The first type of the Pokémon.
    :param str type2: The second type of the Pokémon, which may be the same as type1 if single-typed.
    :param str future_type: The type of the Pokémon at the next evolution stage.
    :param list[str] list_name: The wiki template to add formatted moves to.
    """
    for move in moves:
        tm_data = tm_info(move)

        if _is_stab(tm_data, type1, type2):
            list_name.append("{{MoveTM+|TM" + tm_data["TMNo"] + "|'''}}")
        elif _is_stab(tm_data, future_type, future_type):
            list_name.append("{{MoveTM+|TM" + tm_data["TMNo"] + "|''}}")
        else:
            list_name.append("{{MoveTM+|TM" + tm_data["TMNo"] + "}}")


def _add_breed_moves_to_list(moves, breed_string, type1, type2, future_type, list_name):
    """
    Adds moves a Pokémon may learn by breeding to a given list in wiki format, accounting for STAB and parentage.

    The first Pokémon in an evolution line may be given Egg Moves in pokemon.txt, and these are learnable from any
    fathers that have that move and are in the same Egg Group. Only Smeargle parentage is currently handled. Sorted
    alphabetically.

    :param list[str] moves: A list of egg moves a Pokémon may learn through breeding.
    :param str breed_string: A formatted string indicating the parents to get the egg moves from.
    :param str type1: The first type of the Pokémon.
    :param str type2: The second type of the Pokémon, which may be the same as type1 if single-typed.
    :param str future_type: The type of the Pokémon at the next evolution stage.
    :param list[str] list_name: The wiki template to add formatted moves to.
    """
    for move in sorted(moves):
        move_data = move_info(move)

        if _is_stab(move_data, type1, type2):
            list_name.append("{{MoveBreed+|" + breed_string + "|" + move_data["Name"] + "|'''}}")
        elif _is_stab(move_data, future_type, future_type):
            list_name.append("{{MoveBreed+|" + breed_string + "|" + move_data["Name"] + "|''}}")
        else:
            list_name.append("{{MoveBreed+|" + breed_string + "|" + move_data["Name"] + "}}")


def _add_tutor_moves_to_list(moves, type1, type2, future_type, list_name):
    """
    Adds moves a Pokémon learns by tutoring to a given list in wiki format, accounting for STAB.

    Tutor moves are stored in tm.txt just like TMs, but are outside the TM range of 01-95. They are always teachable
    through the Virtual Move Tutor (VMT) in the games.

    :param list[str] moves: A list of moves a Pokémon can be tutored in.
    :param str type1: The first type of the Pokémon.
    :param str type2: The second type of the Pokémon, which may be the same as type1 if single-typed.
    :param str future_type: The type of the Pokémon at the next evolution stage.
    :param list[str] list_name: The wiki template to add formatted moves to.
    """
    for move in sorted(moves):
        move_data = move_info(move)

        if _is_stab(move_data, type1, type2):
            list_name.append("{{MoveTutor+|" + move_data["Name"] + "|'''|Varies}}")
        elif _is_stab(move_data, future_type, future_type):
            list_name.append("{{MoveTutor+|" + move_data["Name"] + "|''|Varies}}")
        else:
            list_name.append("{{MoveTutor+|" + move_data["Name"] + "||Varies}}")


class MoveListGenerator:
    """
    A class that generates the different lists of moves that a Pokémon can learn by all methods available, given the
    relevant data. This includes moves learned by level up, TM, breeding, and tutoring. This is all done in wiki format.
    """
    def __init__(self, p_data, tm_list, tutor_list):
        """
        The init method for MoveListGenerator.

        :param dict[str, str] p_data: A dictionary containing all the Pokémon's data in pokemon.txt.
        :param list[str] tm_list: A list of TMs the Pokémon can learn.
        :param list[str] tutor_list: A list of moves the Pokémon can be tutored in.
        """
        self.p_data = p_data
        self.level_list = p_data["Moves"].split(",")
        self.tm_list = tm_list
        self.tutor_list = tutor_list
        self.first_type, self.second_type = get_two_types(p_data)

    def _get_dex_data(self):
        """
        Retrieves information for a specific Pokémon from the Pokémon info dictionary. This is used to find the proper
        name of the Pokémon for formatting the start and end lines of the different move templates.

        :return list[str]: The information for a specific Pokémon from pokemon_info.json.
        """
        return pokemon_info(find_dex_number(self.p_data["RegionalNumbers"]))

    def _create_move_list(self, list_type):
        """
        Contains common functionality for generating the move lists for all types.

        Accesses other methods to produce and return a fully-formatted move list. The type of list to generate is passed
        in as a parameter and handled appropriately.

        :param str list_type: A string representing the type of move list being generated.
        :return list[str]: A fully-formatted move list of type list_type.
        """
        # in keeping with PEP, tm is not capitalised in the program, and so is manually done so here
        header = list_type.upper() if list_type == "tm" else list_type.title()

        dex_data = self._get_dex_data()
        move_list = ["{{Move" + header + "Start|" + dex_data["DisplayName"] + "|" + self.first_type + "|" +
                     self.second_type + "}}"]

        breed_string = ""
        evh = EvolutionHandler(self.p_data)
        chain_pos = evh.get_chain_position()
        # Breeding moves need to be handled differently, as they require a breed string, and may not always be needed.
        if list_type == "breed":
            # Smeargle learns all breeding move by default, so a special string is used to indicate this.
            breed_string = "{{EM|107|Smeargle}} '''WIP'''" if "Field" in self.p_data["Compatibility"] \
                else "'''WIP'''"

            first_evo_name = evh.get_first_evo_stage()
            p_data = DataCollection(first_evo_name).extract_pokemon_data()

            if "EggMoves" in self.p_data:
                moves = self.p_data["EggMoves"].split(",")
            elif chain_pos > 1 and "EggMoves" in p_data:
                moves = p_data["EggMoves"].split(",")
            else:
                move_list.append("{{MoveBreedNone}}")
                move_list.append("{{Move" + header + "End|" + dex_data["DisplayName"] + "|" + self.first_type + "|" +
                                 self.second_type + "}}")
                return move_list
        else:
            # Otherwise, can access other move lists from self
            moves = getattr(self, list_type + "_list")

        future_type = evh.find_future_type()

        if list_type == "level":
            _add_level_moves_to_list(moves, self.first_type, self.second_type, future_type, move_list)
        elif list_type == "tm":
            _add_tm_moves_to_list(moves, self.first_type, self.second_type, future_type, move_list)
        elif list_type == "breed":
            _add_breed_moves_to_list(moves, breed_string, self.first_type, self.second_type, future_type, move_list)
        else:
            _add_tutor_moves_to_list(moves, self.first_type, self.second_type, future_type, move_list)

        move_list.append("{{Move" + header + "End|" + dex_data["DisplayName"] + "|" + self.first_type + "|" +
                         self.second_type + "}}")

        return move_list

    def create_level_learn_list(self):
        """
        Public entry point of the process for creating a level up learn list.

        :return list[str]: A fully-formatted level up learn list.
        """
        return self._create_move_list("level")

    def create_tm_learn_list(self):
        """
        Public entry point of the process for creating a TM learn list.

        :return list[str]: A fully-formatted TM learn list.
        """
        return self._create_move_list("tm")

    def create_breeding_learn_list(self):
        """
        Public entry point of the process for creating a breeding learn list.

        :return list[str]: A fully-formatted breeding learn list.
        """
        return self._create_move_list("breed")

    def create_tutor_learn_list(self):
        """
        Public entry point of the process for creating a tutor learn list.

        :return list[str]: A fully-formatted tutor learn list.
        """
        return self._create_move_list("tutor")
