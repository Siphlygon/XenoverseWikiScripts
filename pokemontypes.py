# pylint: disable=locally-disabled, line-too-long, missing-module-docstring, too-few-public-methods
def _generate_type_chart():
    """
    Generates the type chart for every type in Pokémon Xenoverse, which uses Gen V mechanics and the Sound type.

    :return dict[str, dict[str, int]]: A full type chart.
    """
    type_chart = {
        'Normal': {'Normal': 1, 'Fighting': 2, 'Flying': 1, 'Poison': 1, 'Ground': 1, 'Rock': 1, 'Bug': 1, 'Ghost': 0,
                   'Steel': 1, 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Psychic': 1, 'Ice': 1, 'Dragon': 1,
                   'Dark': 1, 'Fairy': 1, 'Sound': 1},
        'Fighting': {'Normal': 1, 'Fighting': 1, 'Flying': 2, 'Poison': 1, 'Ground': 1, 'Rock': 0.5, 'Bug': 0.5,
                     'Ghost': 1, 'Steel': 1, 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Psychic': 2, 'Ice': 1,
                     'Dragon': 1, 'Dark': 0.5, 'Fairy': 2, 'Sound': 1},
        'Flying': {'Normal': 1, 'Fighting': 0.5, 'Flying': 1, 'Poison': 1, 'Ground': 0, 'Rock': 2, 'Bug': 0.5,
                   'Ghost': 1, 'Steel': 1, 'Fire': 1, 'Water': 1, 'Grass': 0.5, 'Electric': 2, 'Psychic': 1, 'Ice': 2,
                   'Dragon': 1, 'Dark': 1, 'Fairy': 1, 'Sound': 2},
        'Poison': {'Normal': 1, 'Fighting': 0.5, 'Flying': 1, 'Poison': 0.5, 'Ground': 2, 'Rock': 1, 'Bug': 0.5,
                   'Ghost': 1, 'Steel': 1, 'Fire': 1, 'Water': 1, 'Grass': 0.5, 'Electric': 1, 'Psychic': 2, 'Ice': 1,
                   'Dragon': 1, 'Dark': 1, 'Fairy': 0.5, 'Sound': 1},
        'Ground': {'Normal': 1, 'Fighting': 1, 'Flying': 1, 'Poison': 0.5, 'Ground': 1, 'Rock': 0.5, 'Bug': 1,
                   'Ghost': 1, 'Steel': 1, 'Fire': 1, 'Water': 2, 'Grass': 2, 'Electric': 0, 'Psychic': 1, 'Ice': 2,
                   'Dragon': 1, 'Dark': 1, 'Fairy': 1, 'Sound': 1},
        'Rock': {'Normal': 0.5, 'Fighting': 2, 'Flying': 0.5, 'Poison': 0.5, 'Ground': 2, 'Rock': 1, 'Bug': 1,
                 'Ghost': 1, 'Steel': 2, 'Fire': 0.5, 'Water': 2, 'Grass': 2, 'Electric': 1, 'Psychic': 1, 'Ice': 1,
                 'Dragon': 1, 'Dark': 1, 'Fairy': 1, 'Sound': 1},
        'Bug': {'Normal': 1, 'Fighting': 0.5, 'Flying': 2, 'Poison': 1, 'Ground': 0.5, 'Rock': 2, 'Bug': 1, 'Ghost': 1,
                'Steel': 1, 'Fire': 2, 'Water': 1, 'Grass': 0.5, 'Electric': 1, 'Psychic': 1, 'Ice': 1, 'Dragon': 1,
                'Dark': 1, 'Fairy': 1, 'Sound': 1},
        'Ghost': {'Normal': 0, 'Fighting': 0, 'Flying': 1, 'Poison': 0.5, 'Ground': 1, 'Rock': 1, 'Bug': 0.5,
                  'Ghost': 2, 'Steel': 1, 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Psychic': 1, 'Ice': 1,
                  'Dragon': 1, 'Dark': 2, 'Fairy': 1, 'Sound': 1},
        'Steel': {'Normal': 0.5, 'Fighting': 2, 'Flying': 0.5, 'Poison': 0, 'Ground': 2, 'Rock': 0.5, 'Bug': 0.5,
                  'Ghost': 1, 'Steel': 0.5, 'Fire': 2, 'Water': 1, 'Grass': 0.5, 'Electric': 1, 'Psychic': 0.5,
                  'Ice': 0.5, 'Dragon': 0.5, 'Dark': 1, 'Fairy': 0.5, 'Sound': 1},
        'Fire': {'Normal': 1, 'Fighting': 1, 'Flying': 1, 'Poison': 1, 'Ground': 2, 'Rock': 2, 'Bug': 0.5, 'Ghost': 1,
                 'Steel': 0.5, 'Fire': 0.5, 'Water': 2, 'Grass': 0.5, 'Electric': 1, 'Psychic': 1, 'Ice': 0.5,
                 'Dragon': 1, 'Dark': 1, 'Fairy': 0.5, 'Sound': 1},
        'Water': {'Normal': 1, 'Fighting': 1, 'Flying': 1, 'Poison': 1, 'Ground': 1, 'Rock': 1, 'Bug': 1, 'Ghost': 1,
                  'Steel': 0.5, 'Fire': 0.5, 'Water': 0.5, 'Grass': 2, 'Electric': 2, 'Psychic': 1, 'Ice': 0.5,
                  'Dragon': 1, 'Dark': 1, 'Fairy': 1, 'Sound': 2},
        'Grass': {'Normal': 1, 'Fighting': 1, 'Flying': 2, 'Poison': 2, 'Ground': 0.5, 'Rock': 1, 'Bug': 2, 'Ghost': 1,
                  'Steel': 1, 'Fire': 2, 'Water': 0.5, 'Grass': 0.5, 'Electric': 0.5, 'Psychic': 1, 'Ice': 2,
                  'Dragon': 1, 'Dark': 1, 'Fairy': 1, 'Sound': 1},
        'Electric': {'Normal': 1, 'Fighting': 1, 'Flying': 0.5, 'Poison': 1, 'Ground': 2, 'Rock': 1, 'Bug': 1,
                     'Ghost': 1, 'Steel': 0.5, 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 0.5, 'Psychic': 1,
                     'Ice': 1, 'Dragon': 1, 'Dark': 1, 'Fairy': 1, 'Sound': 0.5},
        'Psychic': {'Normal': 1, 'Fighting': 0.5, 'Flying': 1, 'Poison': 1, 'Ground': 1, 'Rock': 1, 'Bug': 2,
                    'Ghost': 2, 'Steel': 1, 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Psychic': 0.5, 'Ice': 1,
                    'Dragon': 1, 'Dark': 2, 'Fairy': 1, 'Sound': 0.5},
        'Ice': {'Normal': 1, 'Fighting': 2, 'Flying': 1, 'Poison': 1, 'Ground': 1, 'Rock': 2, 'Bug': 1, 'Ghost': 1,
                'Steel': 2, 'Fire': 2, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Psychic': 1, 'Ice': 0.5, 'Dragon': 1,
                'Dark': 1, 'Fairy': 1, 'Sound': 1},
        'Dragon': {'Normal': 1, 'Fighting': 1, 'Flying': 1, 'Poison': 1, 'Ground': 1, 'Rock': 1, 'Bug': 1, 'Ghost': 1,
                   'Steel': 1, 'Fire': 0.5, 'Water': 0.5, 'Grass': 0.5, 'Electric': 0.5, 'Psychic': 1, 'Ice': 2,
                   'Dragon': 2, 'Dark': 1, 'Fairy': 2, 'Sound': 0.5},
        'Dark': {'Normal': 1, 'Fighting': 2, 'Flying': 1, 'Poison': 1, 'Ground': 1, 'Rock': 1, 'Bug': 2, 'Ghost': 0.5,
                 'Steel': 1, 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Psychic': 0, 'Ice': 1, 'Dragon': 1,
                 'Dark': 0.5, 'Fairy': 2, 'Sound': 1},
        'Fairy': {'Normal': 1, 'Fighting': 0.5, 'Flying': 1, 'Poison': 2, 'Ground': 1, 'Rock': 1, 'Bug': 0.5,
                  'Ghost': 1, 'Steel': 2, 'Fire': 1, 'Water': 1, 'Grass': 1, 'Electric': 1, 'Psychic': 1, 'Ice': 1,
                  'Dragon': 0, 'Dark': 0.5, 'Fairy': 1, 'Sound': 2},
        'Sound': {'Normal': 1, 'Fighting': 1, 'Flying': 0.5, 'Poison': 1, 'Ground': 1, 'Rock': 1, 'Bug': 1,
                  'Ghost': 1, 'Steel': 1, 'Fire': 1, 'Water': 0.5, 'Grass': 1, 'Electric': 2, 'Psychic': 1, 'Ice': 1,
                  'Dragon': 2, 'Dark': 1, 'Fairy': 0.5, 'Sound': 1}
    }
    return type_chart


class TypeEffectivenessCalculator:
    """
    Not empty
    """
    def __init__(self, type1, type2):
        """
        The init function for TypeEffectivenessCalculator

        :param str type1: The first type of the Pokémon.
        :param str type2: The second type of the Pokémon, which may be the same as type1.
        """
        self.type1 = type1
        self.type2 = type2

    def calculate_type_effectiveness(self):
        """


        :return:
        """
        type_chart = _generate_type_chart()

        # Retrieves the match up information for the first type
        first_match_ups = type_chart[self.type1]

        # Dual typing may need to be taken into account
        if self.type2 != self.type1:
            second_match_ups = type_chart[self.type2]

            final_match_ups = {}
            for first_type in first_match_ups.items():
                # if the second type does not affect a particular match up, just use the first type
                if first_type[0] not in second_match_ups:
                    final_match_ups[first_type[0]] = first_type[1]
                else:
                    second_type = second_match_ups[first_type[0]]
                    final_match_ups[first_type[0]] = first_type[1] * second_type

            return final_match_ups

        return first_match_ups
