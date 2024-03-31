# pylint: disable=line-too-long, missing-module-docstring, F0401, too-many-branches, too-many-return-statements
from data_access import evolution_info, pokemon_info, move_info
from utility_methods import find_dex_number
from data_collection import DataCollection


def _is_in_evolution_chain(evol_info):
    """
    Evaluates whether a Pokémon is in an evolution chain - i.e., if it evolves from or into another Pokémon.

    :param dict[str, str | list[str] | dict[str, str]] evol_info: A dictionary containing the evolution information.
    :return bool: Whether the Pokémon is in an evolution chain.
    """
    if evol_info["Evolution"][0] == "no" and evol_info["PreEvolution"] == "no":
        return False
    return True


def _find_first_stage(evol_info):
    """
    Finds the first stage of the Pokémon's evolution chain.

    :param dict[str, str | list[str] | dict[str, str]] evol_info: The information for the current stage of the evolution chain.
    :return dict[str, str | list[str] | dict[str, str]]: The information for the first stage of the evolution chain.
    """
    if evol_info["PreEvolution"] == "no":
        return evol_info
    return _find_first_stage(evolution_info(evol_info["PreEvolution"]))


def _determine_next_stage(evol_info):
    """
    Determines the next stage of the Pokémon's evolution chain.

    :param dict[str, str | list[str] | dict[str, str]] evol_info: The information for the current stage of the evolution chain.
    :return dict[str, str | list[str] | dict[str, str]]: The information for the next stage of the evolution chain.
    """
    next_evos = evol_info["Evolution"]
    # No further evolution stages
    if next_evos[0] == "no":
        return evol_info
    # No branching evolution stage
    if len(next_evos) == 1:
        return evolution_info(next_evos[0])
    # Branching evolution stage e.g., Tyrogue -> Hitmonlee/Hitmonchan/Hitmontop
    evos = []
    for evo in next_evos:
        evos.append(evolution_info(evo))
    return evos


def _construct_evolution_chain(evol_info, internal_name):
    """
    Constructs an evolution chain for the Pokémon using the reference dictionary.

    First starts by determining if the Pokémon is in an evolution chain. If not, it is a single-stage Pokémon.
    Otherwise, starts at the 1st stage evolution and constructs a chain based on the next stage(s) of evolution.
    Uses the fact that all branching evolutions are final evolutions (i.e., no Wurmple-like evolutions).

    :return dict[str, dict[str, str]]: A dictionary containing the evolution chain of the Pokémon.
    """
    evo_chain = {}
    # Single-stage Pokémon
    if not _is_in_evolution_chain(evol_info):
        evo_chain[1] = {"Name": internal_name, "Method": None}
        return evo_chain, "Linear"

    # Find the first stage of the evolution chain
    evo_1 = _find_first_stage(evol_info)

    # Determine the next stage of the evolution chain
    evo_2 = _determine_next_stage(evo_1)

    # If a list, it's a branching evolution of final forms
    if isinstance(evo_2, list):
        evo_chain[1] = {"Name": evo_2[0]["PreEvolution"], "Method": evo_2[0]["PreEvolutionMethod"]}
        for i in range(len(evo_2)):
            evo_chain[i+2] = {"Name": evo_1["Evolution"][i],
                              "Method": evo_2[i + 1]["PreEvolutionMethod"] if i < len(evo_2) - 1 else None}
        branch_info = f"1branch{len(evo_2)}"

    # Else, next evolution is a single evolution, but may have further branching forms
    else:
        # Determine the final evolution stage
        evo_3 = _determine_next_stage(evo_2)
        # If the final evolution is the same as the next evolution, it's a single evolution
        if evo_3 == evo_2:
            evo_chain[1] = {"Name": evo_2["PreEvolution"], "Method": evo_2["PreEvolutionMethod"]}
            evo_chain[2] = {"Name": evo_1["Evolution"][0], "Method": None}
            branch_info = "Linear"
        # Else if a list, it's a branching evolution
        elif isinstance(evo_3, list):
            evo_chain[1] = {"Name": evo_2["PreEvolution"], "Method": evo_2["PreEvolutionMethod"]}
            evo_chain[2] = {"Name": evo_1["Evolution"][0], "Method": evo_3[0]["PreEvolutionMethod"]}
            for i in range(len(evo_3)):
                evo_chain[i+3] = {"Name": evo_2["Evolution"][i],
                                  "Method": evo_3[i + 1]["PreEvolutionMethod"] if i < len(evo_3) - 1 else None}
            branch_info = f"2branch{len(evo_3)}"
        # Else, it's a two-stage evolution
        else:
            evo_chain[1] = {"Name": evo_2["PreEvolution"], "Method": evo_2["PreEvolutionMethod"]}
            evo_chain[2] = {"Name": evo_3["PreEvolution"], "Method": evo_3["PreEvolutionMethod"]}
            evo_chain[3] = {"Name": evo_2["Evolution"][0], "Method": None}
            branch_info = "Linear"

    return evo_chain, branch_info


def _create_evo_string(method):
    """
    Creates a string to describe the method of evolution.

    :param dict[str, str] method: The method of evolution.
    :return str: The string describing the method of evolution.
    """
    if method.keys() == {"Level"}:
        return "{{Item|Rare Candy}}<br />{{color|000|Level " + method["Level"] + "}}"
    if method.keys() == {"LevelFemale"}:
        return "{{Item|Rare Candy}}<br />{{color|000|Level " + method["LevelFemale"] + "}}<br><small>(Female)</small>"
    if method.keys() == {"Item"}:
        return "{{Item|" + method["Item"] + "}}<br />{{color|000|" + method["Item"] + "}}"
    if method.keys() == {"ItemMale"}:
        return "{{Item|" + method["ItemMale"] + "}}<br>{{color2|000|" + method["ItemMale"] + "}}}<br><small>(Male)</small>"
    if method.keys() == {"ItemFemale"}:
        return "{{Item|" + method["ItemFemale"] + "}}<br>{{color2|000|" + method["ItemFemale"] + "}}}<br><small>(Female)</small>"
    if method.keys() == {"Happiness"}:
        return "{{Item|Soothe Bell}}<br>'''Level up'''<br>with {{color|000|high friendship}}"
    if method.keys() == {"HappinessDay"}:
        return "{{Item|Soothe Bell}}<br>'''Level up''' at day <br>with {{color|000|high friendship}}"
    if method.keys() == {"HappinessNight"}:
        return "{{Item|Soothe Bell}}<br>'''Level up''' at night <br>with {{color|000|high friendship}}"
    if method.keys() == {"DayHoldItem"}:
        return "{{Item|" + method["DayHoldItem"] + "}}<br>{{color|000|Level up}}<br>holding {{color2|000|" + method["DayHoldItem"] + "}}<br>(Day)"
    if method.keys() == {"NightHoldItem"}:
        return "{{Item|" + method["NightHoldItem"] + "}}<br>{{color|000|Level up}}<br>holding {{color2|000|" + method["NightHoldItem"] + "}}<br>(Night)"
    if method.keys() == {"HasMove"}:
        move = move_info(method["HasMove"])
        return "{{Item|Rare Candy}} + [[File:TM" + move["Type"] + ".png|link=" + move["Name"] + " (move)|20px]]<br>'''Level up'''<br><small>knowing {{mcolor|" + move["Name"] + "}}</small>"
    if method.keys() == {"Location"}:
        return "{{item|Rare Candy}} + {{item|Town Map}}<br>{{color|000|Level up}}<br><small>in the area of<br>{{color2|000|" + method["Location"] + "}}</small>"
    if method.keys() == {"AttackGreater"}:
        return "{{Item|Rare Candy}}{{Item|Power Bracer}}<br>{{color2|000|Level " + method["AttackGreater"] + "}}<br><small>({{color2|000|Attack}} > {{color2|000|Defense}})</small>"
    if method.keys() == {"DefenseGreater"}:
        return "{{Item|Rare Candy}}{{Item|Power Belt}}<br>{{color2|000|Level " + method["DefenseGreater"] + "}}<br><small>({{color2|000|Attack}} > {{color2|000|Defense}})</small>"
    if method.keys() == {"AtkDefEqual"}:
        return "{{Item|Rare Candy}}{{Item|Macho Brace}}<br>{{color2|000|Level " + method["AtkDefEqual"] + "}}<br><small>({{color2|000|Attack}} = {{color2|000|Defense}})</small>"

    # Otherwise, the method is "HasInParty"
    dc = DataCollection(method["HasInParty"])
    p_data = dc.extract_pokemon_data()
    dex_num = find_dex_number(p_data["RegionalNumbers"])
    display_name = pokemon_info(dex_num)["DisplayName"]
    return "{{EM|" + dex_num + "|" + display_name + "}}<br>'''Level up'''<br>with {{color2|000|" + display_name + "}} in party."


def _create_evo_statement_method(method):
    """
    Creates a string to describe the method of evolution.

    :param dict[str, str] method: The method of evolution.
    :return str: The string describing the method of evolution.
    """
    if method.keys() == {"Level"}:
        return f"starting at level {method["Level"]}"
    if method.keys() == {"LevelFemale"}:
        return f"starting at level {method["LevelFemale"]} if female"
    if method.keys() == {"Item"}:
        return "when exposed to a {{Item|" + method["Item"] + "}} " + f"[[{method["Item"]}]]"
    if method.keys() == {"ItemMale"}:
        return "when exposed to a {{Item|" + method["ItemMale"] + "}} " + f"[[{method["ItemMale"]}]] if male"
    if method.keys() == {"ItemFemale"}:
        return "when exposed to a {{Item|" + method["ItemFemale"] + "}} " + f"[[{method["ItemFemale"]}]] if female"
    if method.keys() == {"Happiness"}:
        return "when leveled up with high friendship"
    if method.keys() == {"HappinessDay"}:
        return "when leveled up with high friendship during the day"
    if method.keys() == {"HappinessNight"}:
        return "when leveled up with high friendship during the night"
    if method.keys() == {"DayHoldItem"}:
        return "when leveled up holding a {{Item|" + method["DayHoldItem"] + "}} " + f"[[{method['DayHoldItem']}]] during the day"
    if method.keys() == {"NightHoldItem"}:
        return "when leveled up holding a {{Item|" + method["NightHoldItem"] + "}} " + f"[[{method['NightHoldItem']}]] during the night"
    if method.keys() == {"HasMove"}:
        move = move_info(method["HasMove"])
        return f"when leveled up while knowing [[{move["Name"]} (move)|{move["Name"]}]]"
    if method.keys() == {"Location"}:
        return f"when leveled up in [[{method["Location"]}]]"
    if method.keys() == {"AttackGreater"}:
        return f"starting at level {method["AttackGreater"]} if its Attack is higher than its Defense"
    if method.keys() == {"DefenseGreater"}:
        return f"starting at level {method["DefenseGreater"]} if its Defense is higher than its Attack"
    if method.keys() == {"AtkDefEqual"}:
        return f"starting at level {method["AtkDefEqual"]} if its Attack and Defense are equal"

    # Otherwise, the method is "HasInParty"
    dc = DataCollection(method["HasInParty"])
    p_data = dc.extract_pokemon_data()
    dex_num = find_dex_number(p_data["RegionalNumbers"])
    display_name = pokemon_info(dex_num)["DisplayName"]
    return f"when leveled up with a [[{display_name}]] in the party"


class EvolutionHandler:
    """
    A class that handles the evolution information for a Pokémon.
    """
    def __init__(self, p_data):
        """
        Initialises the EvolutionHandler class.

        :param dict[str, str] p_data: A dictionary containing all the Pokémon's data in pokemon.txt.
        """
        self.internal_name = pokemon_info(find_dex_number(p_data["RegionalNumbers"]))["InternalName"]
        self.evol_info = evolution_info(self.internal_name)
        self.p_data = p_data
        self.first_type = p_data["Type1"].title()
        self.second_type = p_data.get("Type2", self.first_type).title()
        if self.first_type == 'Suono':
            self.first_type = "Sound"
        if self.second_type == 'Suono':
            self.second_type = "Sound"

    def create_evolution_box(self):
        """
        Creates the evolution box for the Pokémon wiki page given relevant information.

        :return list[str]: The wiki code to produce the evolution box.
        """
        evo_chain, branch_info = _construct_evolution_chain(self.evol_info, self.internal_name)

        if branch_info == "Linear":
            evo_box_header = "{{Evobox-" + f"{len(evo_chain)}"
        else:
            evo_box_header = "{{Evobox-" + f"{branch_info}"

        evo_box = [evo_box_header, f"|type1 = {self.first_type}", f"|type2 = {self.second_type}"]
        for key, value in evo_chain.items():
            dc = DataCollection(value["Name"])
            p_data = dc.extract_pokemon_data()
            display_name = pokemon_info(find_dex_number(p_data["RegionalNumbers"]))["DisplayName"]

            first_type = p_data["Type1"].title()
            if first_type == 'Suono':
                first_type = "Sound"
            evo_box.append(f"|type1-{key} = {first_type}")

            if "Type2" in p_data:
                second_type = p_data["Type2"].title()
                if second_type == 'Suono':
                    second_type = "Sound"
                evo_box.append(f"|type2-{key} = {second_type}")

            evo_box.append(f"|image{key} = {display_name.replace(" ", "")}Front.png")
            evo_box.append(f"|name{key} = {display_name}")
            if value["Method"]:
                evo_string = _create_evo_string(value["Method"])
                evo_box.append(f"|evo{key} = {evo_string}")

        evo_box.append("}}")

        return evo_box

    def create_evolution_statement(self):
        """
        Creates a statement describing the Pokémon's evolution chain for the opening paragraph.

        :return str: The statement describing the Pokémon's evolution chain.
        """
        if not _is_in_evolution_chain(self.evol_info):
            return "It is not known to evolve from or into any other Pokémon."

        evo_chain, branch_info = _construct_evolution_chain(self.evol_info, self.internal_name)

        # Find position of the Pokémon in the evolution chain
        chain_pos = 0
        for key, value in evo_chain.items():
            if value["Name"] == self.internal_name:
                chain_pos = key
                break

        # Construct list of Pokémon evolution components for the statement
        evo_list = []
        for i in range(1, len(evo_chain)):
            dc = DataCollection(evo_chain[i+1]["Name"])
            p_data = dc.extract_pokemon_data()
            display_name = pokemon_info(find_dex_number(p_data["RegionalNumbers"]))["DisplayName"]

            evo_method = _create_evo_statement_method(evo_chain[i]["Method"]) if evo_chain[i]["Method"] else None
            evo_list.append(f"[[{display_name}]] {evo_method}")

        # Order of match up of evo method and display name is reversed depending on chain position
        # Create two lists and vary their indexing to allow for this

        preposition = "into" if chain_pos == 1 else "from"
        if chain_pos == 1:
            second_preposition = ", which evolves into"
        else:
            second_preposition = ", which evolves from" if chain_pos == 3 else ", and later evolves into"

        evo_statement = f"It evolves {preposition} {evo_list[1 - chain_pos]}"
        if len(evo_list) == 2:
            evo_statement += f"{second_preposition} {evo_list[2 - chain_pos]}."
        else:
            evo_statement += "."

        return evo_statement
