# pylint: disable=too-many-lines, line-too-long, missing-function-docstring, F0401
"""
Main script for generating a Pokémon's wiki page. The script will ask for the Pokémon's internal name and then access
other classes and functions to facilitate the generation of the wiki page. The script will then continue repeating until
the user decides to stop the script.
"""
import logging
from pokemon import PokemonBoxGenerator
from moves import MoveListGenerator
from locations import LocationDataGenerator
from wiki import WikiPage
from data_collection import DataCollection
from pokemontypes import TypeEffectivenessCalculator
from evolution import EvolutionHandler


def main():
    # Get the name of the Pokémon for the wiki page. This must match the Internal Name in the game files.
    internal_name = input("\nInput the name of the pokemon: ").upper()

    # Extract data from the game files
    dc = DataCollection(internal_name)
    try:
        pokemon_data = dc.extract_pokemon_data()
        tm_data, tutor_data = dc.extract_move_data()
        location_data, loc_nums = dc.extract_encounter_data()
    except ValueError as e:
        print(f"Error: {e}")
        return

    poke_box_gen = PokemonBoxGenerator(pokemon_data)
    move_list_gen = MoveListGenerator(pokemon_data, tm_data, tutor_data)
    location_data_gen = LocationDataGenerator(pokemon_data, location_data, loc_nums)
    type_eff_calc = TypeEffectivenessCalculator(pokemon_data)
    evo_handler = EvolutionHandler(pokemon_data)

    # Generate Wiki page
    wiki_page = WikiPage(poke_box_gen, move_list_gen, location_data_gen, type_eff_calc, evo_handler)
    wiki_page.generate_wiki_page()


if __name__ == "__main__":
    print("This script was made by Siphlygon for the purpose of updating the english Pokémon Xenoverse Wiki.")
    print("Please report any problems to me.")

    # Set up logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

    while True:
        main()
