# pylint: disable=line-too-long, too-many-boolean-expressions, missing-module-docstring, F0401
from data_access import (gender_code, growth_rate, pokemon_info, wild_item_info, ability_info, species_and_dex_entry)
from utility_methods import (make_three_digits, find_dex_number)
from evolution import EvolutionHandler


class PokemonBoxGenerator:
    """
    A class containing all the methods related to formatting extracted data from pokemon.txt for wiki display.
    """
    def __init__(self, p_data):
        """
        The init function of PokemonBoxGenerator.

        :param p_data: A dictionary containing all the Pokémon's data in pokemon.txt.
        """
        self.p_data = p_data
        if p_data["Type1"] == 'SUONO':
            self.first_type = "Sound"
        else:
            self.first_type = p_data["Type1"].title()
        self.second_type = p_data.get("Type2", self.first_type).title()
        if self.second_type == 'Suono':
            self.second_type = "Sound"
        self.name = pokemon_info(find_dex_number(self.p_data["RegionalNumbers"]))["DisplayName"]

    def create_header_footer(self):
        """
        Creates the header/footer for the Pokémon wiki page given relevant information.

        :return list[str]: The wiki code to produce the header/footer.
        """
        head_foot = ["{{PokemonPrevNextHead", "|type = " + self.first_type]

        if self.second_type != self.first_type:
            head_foot.append("|type2 = " + self.second_type)

        dex_num = find_dex_number(self.p_data["RegionalNumbers"])

        # Each dex has different lengths and thus different rules in deciding next/prev.
        def get_prev_next(num, region):
            prev_num = make_three_digits(str(num - 1))
            next_num = make_three_digits(str(num + 1))

            # Defines the boundaries of the dexes
            dex_bounds = {"": 583, "X": 44, "V": 207}

            if num > 1:
                head_foot.append(f"|prev = {pokemon_info(region + prev_num)["DisplayName"]}")
                head_foot.append(f"|prevnum = {region + prev_num}")
            # If the number is 1, it will go to the last number of the dex
            else:
                for reg, bound in dex_bounds.items():
                    if region == reg:
                        head_foot.append(f"|prev = {pokemon_info(reg + make_three_digits(str(bound)))["DisplayName"]}")
                        head_foot.append(f"|prevnum = {reg + make_three_digits(str(bound))}")

            # Deciding next number & pokémon, accounting for the different bounds of each dex
            if num < dex_bounds[region]:
                head_foot.append(f"|next = {pokemon_info(region + next_num)["DisplayName"]}")
                head_foot.append(f"|nextnum = {region + next_num}")
            else:
                head_foot.append(f"|next = {pokemon_info(region + "001")["DisplayName"]}")
                head_foot.append(f"|nextnum = {region + '001'}")

        # Specific range is chosen to obtain only digits and ignore either the region or any alt forms i.e., ABC_1
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
        Creates the infobox for the Pokémon wiki page given relevant information.

        :return list[str]: The wiki code to produce the infobox.
        """
        infobox = ["{{Pokemon Infobox", "|type1 = " + self.first_type]

        if self.second_type != self.first_type:
            infobox.append("|type2 = " + self.second_type)

        # Name, Species
        infobox.append("|name = " + self.name)
        infobox.append("|species = " + species_and_dex_entry(self.p_data["InternalNumber"])["Species"])

        # Dex & Image
        dex_nums = find_dex_number(self.p_data["RegionalNumbers"])
        infobox.append("|ndex = " + dex_nums)
        infobox.append("|image = " + self.name.replace(" ", "") + ".png")

        # Abilities
        reg_abilities = self.p_data["Abilities"].split(",")
        infobox.append("|ability1 = " + ability_info(reg_abilities[0]))
        if len(reg_abilities) > 1:
            infobox.append("|ability2 = " + ability_info(reg_abilities[1]))
        if "HiddenAbility" in self.p_data:
            infobox.append("|hiddenability = " + ability_info(self.p_data["HiddenAbility"]))

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
        metric_height = int(self.p_data["Height"]) / 10
        metric_weight = int(self.p_data["Weight"]) / 10
        infobox.extend(["|height-m = " + str(metric_height),
                        f"|weight-kg =  {metric_weight:g}"])

        # Imperial height & weight
        imperial_height = metric_height * 39.37008
        feet = int(imperial_height // 12)
        inches = round(imperial_height % 12)
        if inches == 12:
            feet += 1
            inches = 0
        imperial_weight = round(metric_weight * 2.20462262, 1)
        infobox.extend([f"|height-ftin = {feet}" + "'" + str(inches).zfill(2) + '"',
                        f"|weight-lbs = {imperial_weight:g}"])

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
        pokedex_entry = ["{{Dex", "|type = " + self.first_type]

        if self.second_type != self.first_type:
            pokedex_entry.append("|type2 = " + self.second_type)

        pokedex_entry.append(f"|''{species_and_dex_entry(self.p_data['InternalNumber'])['Dex Entry']}''")

        pokedex_entry.append("}}")

        return pokedex_entry

    def create_opening_paragraph(self):
        """
        Currently incomplete; creates the opening paragraph for the Pokémon wiki page given relevant information.

        :return list[str]: The wiki code to produce the opening paragraph.
        """
        dual_type = "dual-type " if "Type2" in self.p_data else ""
        typing = "{{Type|" + self.first_type + "}}/{{Type|" + self.second_type + "}}" \
            if "Type2" in self.p_data else "{{Type|" + self.first_type + "}}"

        determiner = "an" if typing[7] in ["E", "I"] else "a"
        opening_paragraph = [f"'''{self.name}''' is {determiner} {dual_type}{typing}-type Pokémon.", ""]

        evh = EvolutionHandler(self.p_data)
        evo_statement = evh.create_evolution_statement()
        opening_paragraph.append(evo_statement)

        return opening_paragraph

    def create_wild_items(self):
        """
        Creates the wild held item box for the Pokémon wiki page given relevant information.

        :return list[str]: The wiki code to produce the wild held item box.
        """
        wild_items = ["{{HeldItems", "|type = " + self.first_type]

        if self.second_type != self.first_type:
            wild_items.append("|type2 = " + self.second_type)

        item_slots = ["Common", "Uncommon", "Rare"]

        found_items = []
        temp_box = []
        # Check and add items for each rarity slot
        for slot in item_slots:
            if f"WildItem{slot}" in self.p_data:
                item = wild_item_info(self.p_data[f"WildItem{slot}"])
                temp_box.append(f"|{slot.lower()} = " + "{{Item|" + item + "}} " + f"[[{item}]]")
                found_items.append(item)

        # Accounts for how the game data indicates a 100% item
        if len(set(found_items)) == 1 and len(found_items) == 3:
            wild_items.append("|always = " + "{{Item|" + found_items[0] + "}} " + f"[[{found_items[0]}]]")
        else:
            wild_items.extend(temp_box)

        wild_items.append("}}")

        return wild_items

    def create_stats(self):
        """
        Creates the stats box for the Pokémon wiki page given relevant information.

        :return list[str]: The wiki code to produce the stats box.
        """
        stats = ["{{Stats", "|type = " + self.first_type]

        if self.second_type != self.first_type:
            stats.append("|type2 = " + self.second_type)

        # Stats are given in HP/ATK/DEF/SPE/SPA/SPD order
        stat_names = ["HP", "Attack", "Defense", "Speed", "SpAtk", "SpDef"]
        raw_stats = self.p_data["BaseStats"].split(",")

        # Add each stat to the stats box
        for name, value in zip(stat_names, raw_stats):
            stats.append(f"|{name} = {value}")

        stats.append("}}")

        return stats

    def create_sprites(self):
        """
        Currently incomplete; creates the type effectiveness box for the Pokémon wiki page given relevant information.

        :return list[str]: The wiki code to produce the type effectiveness box.
        """
        sprites = ["{{sprites|name=" + self.name.replace(" ", "") + "|type=" + self.first_type + "|type2=" +
                   self.second_type + "}}"]

        return sprites
