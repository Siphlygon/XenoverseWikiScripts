# pylint: disable=locally-disabled, line-too-long, missing-module-docstring, too-few-public-methods


class WikiPage:
    """
    Simple class collating different methods together in order to print a full wiki page for a certain Pokémon.
    """
    def __init__(self, pokemon, move, location):
        """
        The init function of WikiPage.

        :param class pokemon: An initialised Pokémon class.
        :param class move: An initialised Move class.
        :param class location: An initialised Location class.
        """
        self.pokemon = pokemon
        self.move = move
        self.location = location

    def generate_wiki_page(self):
        """
        Retrieves and prints the different elements of a Pokémon wiki page in a pre-defined order.
        """
        # Create the necessary components of the pokemon wiki page
        header_footer = self.pokemon.create_header_footer()
        info_box = self.pokemon.create_infobox()
        open_para = self.pokemon.create_opening_paragraph()

        # Define section titles
        section_titles = {
            "Pokédex entries": self.pokemon.create_pokedex_entry(),
            "Game locations": self.location.create_game_locations(),
            "Held items": self.pokemon.create_wild_items(),
            "Stats": self.pokemon.create_stats(),
            "Type effectiveness": self.pokemon.create_type_effectiveness(),
            "Learnset": {
                "By leveling up": self.move.create_level_learn_list(),
                "By TM/HM": self.move.create_tm_learn_list(),
                "By breeding": self.move.create_breeding_learn_list(),
                "By tutoring": self.move.create_tutor_learn_list()
            },
            "Evolution": self.pokemon.create_evolution_line(),
            "Sprites": self.pokemon.create_sprites()
        }

        # Assemble wiki page
        wiki_page = []
        wiki_page.extend(header_footer)
        wiki_page.extend(info_box)
        wiki_page.extend(open_para)

        for title, content in section_titles.items():
            wiki_page.append(f"=='''{title}'''==")
            if isinstance(content, dict):
                for subtitle, subcontent in content.items():
                    wiki_page.append(f"==='''{subtitle}'''===")
                    wiki_page.extend(subcontent)
            else:
                wiki_page.extend(content)

        wiki_page.extend(header_footer)

        # Print wiki page
        for line in wiki_page:
            print(line)
