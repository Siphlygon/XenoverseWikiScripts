# pylint: disable=line-too-long, missing-module-docstring, too-few-public-methods, too-many-arguments


class WikiPage:
    """
    Simple class collating different methods together in order to print a full wiki page for a certain Pokémon.
    """
    def __init__(self, poke_box_gen, move_list_gen, location_data_gen, type_eff_calc, evo_handler):
        """
        The init function of WikiPage.

        :param class poke_box_gen: An initialised PokémonBoxGenerator class.
        :param class move_list_gen: An initialised MoveListGenerator class.
        :param class location_data_gen: An initialised LocationDataGenerator class.
        :param class type_eff_calc: An initialised TypeEffectivenessCalculator class.
        :param class evo_handler: An initialised EvolutionHandler class.
        """
        self.poke_box_gen = poke_box_gen
        self.move_list_gen = move_list_gen
        self.location_data_gen = location_data_gen
        self.type_eff_calc = type_eff_calc
        self.evo_handler = evo_handler

    def generate_wiki_page(self):
        """
        Retrieves and prints the different elements of a Pokémon wiki page in a pre-defined order.
        """
        # Create the necessary components of the pokemon wiki page
        header_footer = self.poke_box_gen.create_header_footer()
        info_box = self.poke_box_gen.create_infobox()
        open_para = self.poke_box_gen.create_opening_paragraph()

        # Define section titles
        section_titles = {
            "Pokédex entries": self.poke_box_gen.create_pokedex_entry(),
            "Game locations": self.location_data_gen.create_game_locations(),
            "Held items": self.poke_box_gen.create_wild_items(),
            "Stats": self.poke_box_gen.create_stats(),
            "Type effectiveness": self.type_eff_calc.create_type_effectiveness(),
            "Learnset": {
                "By leveling up": self.move_list_gen.create_level_learn_list(),
                "By TM/HM": self.move_list_gen.create_tm_learn_list(),
                "By breeding": self.move_list_gen.create_breeding_learn_list(),
                "By tutoring": self.move_list_gen.create_tutor_learn_list()
            },
            "Evolution": self.evo_handler.create_evolution_box(),
            "Sprites": self.poke_box_gen.create_sprites()
        }

        # Assemble wiki page
        wiki_page = []
        wiki_page.extend(header_footer)
        wiki_page.extend(info_box)
        wiki_page.extend(open_para)
        wiki_page.append("")

        for title, content in section_titles.items():
            wiki_page.append(f"=='''{title}'''==")
            if isinstance(content, dict):
                for subtitle, subcontent in content.items():
                    wiki_page.append(f"==='''{subtitle}'''===")
                    wiki_page.extend(subcontent)
            else:
                wiki_page.extend(content)

        wiki_page.extend(["", ""])
        wiki_page.extend(header_footer)

        # Print wiki page
        for line in wiki_page:
            print(line)
