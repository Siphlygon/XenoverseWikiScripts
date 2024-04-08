# pylint: disable=line-too-long, missing-module-docstring, import-error, too-many-arguments
import json
from data_collection import DataCollection

# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{pbar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


def load_dictionary_data(filename):
    """
    Load a dictionary from a JSON file.

    :param filename: The name of the JSON file to load.
    :return: The loaded dictionary.
    """
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    print("This is a special script to create lists of certain types for all Pokémon in Xenoverse.")

    # Local versions of reference dictionaries are used here
    pokemon = load_dictionary_data("pokemon_info.json")
    ability_info = load_dictionary_data("ability_info.json")
    wild_item_info = load_dictionary_data("wild_item_info.json")
    static_encounters = load_dictionary_data("static_encounters.json")

    # Set up the list types
    list_types = {
        "EVYield": [],
        "Ability": [],
        "BaseStats": [],
        "EncDropList": [],
        "UnEncDropList": []
    }

    print("Starting data extraction...")
    l = len(pokemon)
    print_progress_bar(0, l, prefix='Progress:', suffix='Complete', length=50)
    for i, (key, value) in enumerate(pokemon.items()):
        print_progress_bar(i+1, l, prefix='Progress:', suffix='Complete', length=50)
        internal_name = value.split(",")[0]
        display_name = value.split(",")[1]
        dc = DataCollection(internal_name, "../../gamedata/pokemon.txt", encounters_path="../../gamedata/encounters.txt")
        p_data = dc.extract_pokemon_data()
        e_data, _ = dc.extract_encounter_data()

        # List by EV Yield
        EVYield = p_data["EffortPoints"].split(",")
        EVYield[3], EVYield[5] = EVYield[5], EVYield[3]  # Order is currently HP/ATK/DEF/SPE/SPA/SPDEF
        EVYield[3], EVYield[4] = EVYield[4], EVYield[3]  # Order is now HP/ATK/DEF/SPA/SPDEF/SPE
        list_types["EVYield"].append("{{BaseStatsListEntry|" + key + "|" + display_name + "|" + "|".join(EVYield) + "}}")

        # List by Ability
        abilities = p_data["Abilities"].split(",")
        if len(abilities) == 1:
            abilities.append("")
        abilities.append(p_data.get("HiddenAbility", ""))
        formatted_abilities = [ability_info[ability] for ability in abilities]
        list_types["Ability"].append("{{AbilityListEntry|" + key + "|" + display_name + "|" + "|".join(formatted_abilities) + "}}")

        # List by Base Stats
        base_stats = p_data["BaseStats"].split(",")
        base_stats[3], base_stats[5] = base_stats[5], base_stats[3]  # Make sure the order is HP, Atk, Def, SpA, SpD, Spe
        list_types["BaseStats"].append("{{BaseStatsListEntry|" + key + "|" + display_name + "|" + "|".join(base_stats) + "}}")

        # Pokémon Drop List
        item_slots = ["Common", "Uncommon", "Rare"]
        item_found = False
        items = []
        for slot in item_slots:
            if f"WildItem{slot}" in p_data:
                wild_item = wild_item_info[p_data[f"WildItem{slot}"]]
                items.append("{{Item|{{{1|" + wild_item + "}}}}}")
                item_found = True
            else:
                items.append("")
        if not item_found:
            continue

        # Check if all items are the same; then it's guaranteed, which is represented as the 4th position
        if len(set(items)) == 1 and len(items) == 3:
            items = ["", "", "", items[0]]

        # Some names need to be edited such that they don't break the template
        display_name = "Bremand_V" if display_name == "Bremand" else display_name
        display_name = "Zorua_H" if display_name == "Zorua" else display_name
        split_name = display_name.split(" ")
        if split_name[-1] == "X":
            display_name = split_name[0] + "X"
            if split_name[0] == "Pikachu":
                display_name += "M"

        # Account for some vintage pokémon
        if split_name[0] == "Vintage":
            v_e_data = DataCollection(split_name[1], encounters_path="../../gamedata/encounters.txt").extract_encounter_data()
            if not e_data:
                e_data = v_e_data

        # Encounterable test
        unencounterable_statics = ("Gift", "Trade", "Fossil")
        if (internal_name in static_encounters and static_encounters[internal_name] not in unencounterable_statics) or e_data:
            list_types["EncDropList"].append("{{HeldItemsEntry|" + display_name + "|" + "|".join(items) + "}}")
        else:
            list_types["UnEncDropList"].append("{{HeldItemsEntry|" + display_name + "|" + "|".join(items) + "}}")

    print("Saving data...")
    for key, value in list_types.items():
        with open(key.lower() + "_list.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(value))

    print("Finished! The lists have been exported to appropriate files.")
