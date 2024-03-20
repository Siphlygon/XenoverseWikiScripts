# pylint: disable=locally-disabled, line-too-long, too-many-boolean-expressions, missing-module-docstring
from data_access import (gender_code, growth_rate, pokemon_info, item_info)
from utility_methods import (make_three_digits, find_dex_number)


class PokemonBoxGenerator:
    """
    A class containing all the methods related to extracting data from pokemon.txt for a Pokémon.
    """
    def __init__(self, p_data):
        """
        The init function of Pokemon.

        :param p_data: A dictionary containing all the Pokemon's data in pokemon.txt.
        """
        self.p_data = p_data
        self.first_type = p_data["Type1"].title()
        self.second_type = p_data.get("Type2", self.p_data["Type1"]).title()

    def create_header_footer(self):
        """
        Creates the header/footer for the Pokémon given relevant information.

        :return list[str]: The wiki code to produce the header/footer.
        """
        head_foot = ["{{PokemonPrevNextHead", "|type = " + self.first_type, "|type2 = " + self.second_type]

        dex_num = find_dex_number(self.p_data["RegionalNumbers"])

        # Each dex has different lengths and thus different rules in deciding next/prev.
        def get_prev_next(num, region):
            prev_num = make_three_digits(str(num - 1))
            next_num = make_three_digits(str(num + 1))

            # Deciding previous number & pokémon, across dexes
            if num > 1:
                head_foot.append(f"|prev = {pokemon_info(region + prev_num).split(',')[1]}")
                head_foot.append(f"|prevnum = {region + prev_num}")
            elif region == "X":
                head_foot.append(f"|prev = {pokemon_info('583').split(',')[1]}")
                head_foot.append("|prevnum = 583")
            elif region == "V":
                head_foot.append(f"|prev = {pokemon_info('X044').split(',')[1]}")
                head_foot.append("|prevnum = X044")

            # Deciding next number & pokémon, across dexes
            if (region == "" and num < 583) or (region == 'V' and num < 207) or (region == 'X' and num < 44):
                head_foot.append(f"|next = {pokemon_info(region + next_num).split(',')[1]}")
                head_foot.append(f"|nextnum = {region + next_num}")
            elif region == "":
                head_foot.append(f"|next = {pokemon_info('X001').split(',')[1]}")
                head_foot.append("|nextnum = X001")
            elif region == "X":
                head_foot.append(f"|next = {pokemon_info('V001').split(',')[1]}")
                head_foot.append("|nextnum = V001")

        if dex_num[0] == "X":
            get_prev_next(int(dex_num[1:4]), "X")
        elif dex_num[0] == "V":
            get_prev_next(int(dex_num[1:4]), "V")
        else:
            get_prev_next(int(dex_num[:3]), "")

        head_foot.append("}}")

        return head_foot

    def create_infobox(self):
        """
        Creates the infobox for the Pokémon given relevant information.

        :return list[str]: The wiki code to produce the infobox.
        """
        infobox = ["{{Pokemon Infobox", "|type1 = " + self.first_type, "|type2 = " + self.second_type]

        # Name, Species
        dex_data = pokemon_info(find_dex_number(self.p_data["RegionalNumbers"]))
        infobox.append("|name = " + dex_data.split(",")[1])
        infobox.append("|species = Species Name")

        # Dex & Image
        dex_nums = find_dex_number(self.p_data["RegionalNumbers"])
        infobox.append("|ndex = " + dex_nums)
        infobox.append("|image = " + self.p_data["Name"] + ".png")

        # Abilities
        reg_abilities = self.p_data["Abilities"].split(",")
        infobox.append("|ability1 = " + reg_abilities[0].title())
        if len(reg_abilities) > 1:
            infobox.append("|ability2 = " + reg_abilities[1].title())
        if "HiddenAbility" in self.p_data:
            infobox.append("|hiddenability = " + self.p_data["HiddenAbility"].title())

        # Gender, Catch Rate
        infobox.extend(["|gendercode = " + gender_code(self.p_data["GenderRate"]),
                        "|catchrate = " + self.p_data["Rareness"]])

        # Egg Groups & Steps
        egg_groups = self.p_data["Compatibility"].split(",")
        infobox.append("|egggroup1 = " + egg_groups[0])
        if len(egg_groups) > 1:
            infobox.append("|egggroup2 = " + egg_groups[1])
        infobox.append("|eggsteps = " + self.p_data["StepsToHatch"])

        # Metric height & weight
        infobox.extend(["|height-m = " + str(int(self.p_data["Height"]) / 10),
                        "|weight-kg = " + str(int(self.p_data["Weight"]) / 10)])

        # Exp Yield & Level Rate
        infobox.extend(["|expyield = " + self.p_data["BaseEXP"], "|lvrate = " + growth_rate(self.p_data["GrowthRate"])])

        # Colour & Friendship
        infobox.extend(["|color = " + self.p_data["Color"], "|friendship = " + self.p_data["Happiness"]])

        # EVs
        evs = self.p_data["EffortPoints"].split(",")
        ev_types = ["hp", "at", "de", "sp", "sa", "sd"]
        for i, ev in enumerate(evs):
            if ev != "0":
                infobox.append(f"|ev{ev_types[i]} = {ev}")

        infobox.append("}}")

        return infobox

    def create_pokedex_entry(self):
        """
        Currently incomplete; just creates an empty Pokédex entry.

        :return list[str]: The wiki code to produce the Pokédex entry.
        """
        pokedex_entry = ["{{Dex", "|type = " + self.first_type, "|type2 = " + self.second_type, "''WIP''", "}}"]

        return pokedex_entry

    def create_opening_paragraph(self):
        """
        Currently incomplete; creates the opening paragraph for the Pokémon given relevant information.

        :return list[str]: The wiki code to produce the opening paragraph.
        """
        dual_type = "dual-type" if "Type2" in self.p_data else ""
        typing = "{{Type|" + self.first_type + "}}/{{Type|" + self.second_type + "}}" \
            if "Type2" in self.p_data else "{{Type|" + self.first_type + "}}"
        opening_paragraph = [f"'''{self.p_data['Name']}''' is a {dual_type} {typing}-type Pokémon."]

        return opening_paragraph

    def create_wild_items(self):
        """
        Creates the wild held item box for the Pokémon given relevant information.

        :return list[str]: The wiki code to produce the wild held item box.
        """
        wild_items = ["{{HeldItems", "|type = " + self.first_type, "|type2 = " + self.second_type]

        item_slots = ["Common", "Uncommon", "Rare"]

        # Check and add items for each rarity slot
        for slot in item_slots:
            if f"WildItem{slot}" in self.p_data:
                item = item_info(self.p_data[f"WildItem{slot}"])
                wild_items.append(f"|{slot.lower()} = {{Item|{item}}} [[{item}]]")

        wild_items.append("}}")

        return wild_items

    def create_stats(self):
        """
        Creates the stats box for the Pokémon given relevant information.

        :return list[str]: The wiki code to produce the stats box.
        """
        stats = ["{{Stats", "|type = " + self.first_type, "|type2 = " + self.second_type]

        # Stats are given in HP/ATK/DEF/SPE/SPA/SPD order
        stat_names = ["HP", "Attack", "Defense", "Speed", "SpAtk", "SpDef"]
        raw_stats = self.p_data["BaseStats"].split(",")

        # Add each stat to the stats box
        for name, value in zip(stat_names, raw_stats):
            stats.append(f"|{name} = {value}")

        stats.append("}}")

        return stats

    def create_type_effectiveness(self):
        """
        Currently incomplete; creates the type effectiveness box for the Pokémon given relevant information.

        :return list[str]: The wiki code to produce the type effectiveness box.
        """
        type_effectiveness = ["{{TypeEffectiveness", "|type1 = " + self.first_type, "|type2 = " + self.second_type,
                              "}}"]

        return type_effectiveness

    def create_evolution_line(self):
        """
        Creates the type effectiveness box for the Pokémon given relevant information.

        :return list[str]: The wiki code to produce the type effectiveness box.
        """
        evo_line = ["{{Evobox-1", "|type1 = " + self.first_type, "|type2 = " + self.second_type,
                    "|type1-1 = " + self.first_type, "|type2-1 = " + self.second_type,
                    "|image1 = " + self.p_data["Name"] + ".png", "|name1 = " + self.p_data["Name"], "}}"]

        return evo_line

    def create_sprites(self):
        """
        Currently incomplete; creates the type effectiveness box for the Pokémon given relevant information.

        :return list[str]: The wiki code to produce the type effectiveness box.
        """
        sprites = ["{{sprites|name=" + self.p_data["Name"] + "|type="+ self.first_type + "|type2="+ self.second_type + "}}"]

        return sprites