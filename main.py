# pylint: disable=locally-disabled, too-many-lines, line-too-long
"""
Not empty
"""

from pokemon import PokemonBoxGenerator
from moves import MoveListGenerator
from locations import LocationDataGenerator
from wiki import WikiPage
from data_collection import DataCollection
from pokemontypes import TypeEffectivenessCalculator


def main():
    # Get the name of the Pokémon for the wiki page
    internal_name = input("\nInput the name of the pokemon: ").upper()

    # Create instance
    dc = DataCollection(internal_name)

    # Get pokemon, move, and location data
    pokemon_data = dc.extract_pokemon_data()
    tm_data, tutor_data = dc.extract_move_data()
    location_data, loc_nums = dc.extract_encounter_data()

    # Create instances
    poke_box_gen = PokemonBoxGenerator(pokemon_data)
    move_list_gen = MoveListGenerator(pokemon_data, tm_data, tutor_data)
    location_data_gen = LocationDataGenerator(pokemon_data, location_data, loc_nums)
    type_eff_calc = TypeEffectivenessCalculator(pokemon_data)

    # Generate Wiki page
    wiki_page = WikiPage(poke_box_gen, move_list_gen, location_data_gen, type_eff_calc)
    wiki_page.generate_wiki_page()


if __name__ == "__main__":
    print("This script was made by Siphlygon for the purpose of updating the english Pokémon Xenoverse Wiki.")
    print("Please report any problems to me.")

    while True:
        main()
