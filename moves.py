# pylint: disable=locally-disabled, too-many-lines, line-too-long, missing-module-docstring
from data_access import (pokemon_info, move_info, tm_info)
from utility_methods import find_dex_number


def _if_stab(move_data, type1, type2):
    """
    Decides if a move will gain a Same Type Attack Bonus (STAB) when used by the Pokémon. This occurs if the move's type
    is the same as one of the Pokémon's.

    :param list[str] move_data: The data relating to the move being considered.
    :param str type1: The first type of the Pokémon.
    :param str type2: The second type of the Pokémon, which may be the same as type1.
    :return bool: If the move will gain STAB when used.
    """
    return move_data[1] == "yes" and (move_data[2] == type1 or move_data[2] == type2)


def _add_level_moves_to_list(moves, type1, type2, list_name):
    """
    Adds moves a Pokémon learns by level up to a given list in wiki format, accounting for STAB and indicating level.

    :param list[str] moves: A list of levels and moves learned at those levels in sequential order.
    :param str type1: The first type of the Pokémon.
    :param str type2: The second type of the Pokémon, which may be the same as type1.
    :param list[str] list_name: The list to add formatted moves to.
    """
    for x in range(0, len(moves) - 1, 2):
        move_data = move_info(moves[x + 1]).split(",")

        if _if_stab(move_data, type1, type2):
            list_name.append("{{MoveLevel+|" + moves[x] + "|" + move_data[0] + "|'''}}")
        else:
            list_name.append("{{MoveLevel+|" + moves[x] + "|" + move_data[0] + "}}")


def _add_tm_moves_to_list(moves, type1, type2, list_name):
    """
    Adds moves a Pokémon learns by TM to a given list in wiki format, accounting for STAB and indicating TM number.

    :param list[str] moves: A list of TM moves learnable by a Pokémon.
    :param str type1: The first type of the Pokémon.
    :param str type2: The second type of the Pokémon, which may be the same as type1.
    :param list[str] list_name: The list to add formatted moves to.
    """
    for move in moves:
        tm_data = tm_info(move).split(",")

        if _if_stab(tm_data, type1, type2):
            list_name.append("{{MoveTM+|TM" + tm_data[0] + "|'''}}")
        else:
            list_name.append("{{MoveTM+|TM" + tm_data[0] + "}}")


def _add_breed_moves_to_list(moves, breed_string, type1, type2, list_name):
    """
    Adds moves a Pokémon may learn by breeding to a given list in wiki format, accounting for STAB and parentage.

    :param list[str] moves: A list of egg moves a Pokémon may learn through breeding.
    :param str breed_string: A formatted string indicating the parents to get the egg moves from.
    :param str type1: The first type of the Pokémon.
    :param str type2: The second type of the Pokémon, which may be the same as type1.
    :param list[str] list_name: The list to add formatted moves to.
    """
    for move in sorted(moves):
        move_data = move_info(move).split(",")

        if _if_stab(move_data, type1, type2):
            list_name.append("{{MoveBreed+|" + breed_string + "|" + move_data[0] + "|'''}}")
        else:
            list_name.append("{{MoveBreed+|" + breed_string + "|" + move_data[0] + "}}")


def _add_tutor_moves_to_list(moves, type1, type2, list_name):
    """
    Adds moves a Pokémon learns by tutoring (VMT) to a given list in wiki format, accounting for STAB.

    :param list[str] moves: A list of moves a Pokémon can be tutored in.
    :param str type1: The first type of the Pokémon.
    :param str type2: The second type of the Pokémon, which may be the same as type1.
    :param list[str] list_name: The list to add formatted moves to.
    """
    for move in sorted(moves):
        move_data = move_info(move).split(",")

        if _if_stab(move_data, type1, type2):
            list_name.append("{{MoveTutor+|" + move_data[0] + "|'''|Varies}}")
        else:
            list_name.append("{{MoveTutor+|" + move_data[0] + "||Varies}}")


class MoveListGenerator:
    """
    A class that generates the different lists of moves that a Pokémon can learn by all methods available.
    """
    def __init__(self, p_data, tm_list, tutor_list):
        """
        The init method for MoveListGenerator.

        :param dict[str, str] p_data: A dictionary containing all the Pokémon's data in pokemon.txt.
        :param list[str] tm_list: A list of TMs the Pokémon can learn.
        :param list[str] tutor_list: A list of moves the Pokémon can be tutored.
        """
        self.p_data = p_data
        self.level_list = self.p_data["Moves"].split(",")
        self.tm_list = tm_list
        self.tutor_list = tutor_list
        self.first_type = p_data["Type1"].title()
        self.second_type = p_data.get("Type2", self.p_data["Type1"]).title()

    def _get_dex_data(self):
        """
        Retrieves information for a specific Pokémon.

        :return list[str]: The information for a specific Pokémon.
        """
        return pokemon_info(find_dex_number(self.p_data["RegionalNumbers"])).split(",")

    def _create_move_list(self, list_type):
        """
        Contains common functionality for generating the move lists for all types. Accesses other methods to produce
        and return a fully-formatted move list.

        :param str list_type: A string representing the type of move list being generated.
        :return list[str]: A fully-formatted move list of type list_type.
        """
        dex_data = self._get_dex_data()
        header = list_type.upper() if list_type == "tm" else list_type.title()
        move_list = ["{{Move" + header + "Start|" + dex_data[1] + "|" + self.first_type + "|" +
                     self.second_type + "}}"]

        # Breeding moves need to be handled differently
        if list_type == "breed":
            if "EggMoves" in self.p_data:
                breed_string = "{{EM|107|Smeargle}} '''WIP'''" if "Field" in self.p_data["Compatibility"]\
                    else "'''WIP'''"
                moves = self.p_data["EggMoves"].split(",")
            else:
                move_list.append("{{MoveBreedNone}}")
                move_list.append("{{Move" + header + "End|" + dex_data[1] + "|" + self.first_type + "|" +
                                 self.second_type + "}}")
                return move_list
        else:
            # Otherwise, can access other move lists from self
            moves = getattr(self, list_type + "_list")

        if list_type == "level":
            _add_level_moves_to_list(moves, self.first_type, self.second_type, move_list)
        elif list_type == "tm":
            _add_tm_moves_to_list(moves, self.first_type, self.second_type, move_list)
        elif list_type == "breed" and "EggMoves" in self.p_data:
            _add_breed_moves_to_list(moves, breed_string, self.first_type, self.second_type, move_list)
        else:
            _add_tutor_moves_to_list(moves, self.first_type, self.second_type, move_list)

        move_list.append("{{Move" + header + "End|" + dex_data[1] + "|" + self.first_type + "|" +
                         self.second_type + "}}")

        return move_list

    def create_level_learn_list(self):
        """
        Entry point of the process for creating a level up learn list.

        :return list[str]: A fully-formatted level up learn list.
        """
        return self._create_move_list("level")

    def create_tm_learn_list(self):
        """
        Entry point of the process for creating a TM learn list.

        :return list[str]: A fully-formatted TM learn list.
        """
        return self._create_move_list("tm")

    def create_breeding_learn_list(self):
        """
        Entry point of the process for creating a breeding learn list.

        :return list[str]: A fully-formatted breeding learn list.
        """
        return self._create_move_list("breed")

    def create_tutor_learn_list(self):
        """
        Entry point of the process for creating a tutor learn list.

        :return list[str]: A fully-formatted tutor learn list.
        """
        return self._create_move_list("tutor")
