# pylint: disable=locally-disabled, line-too-long, missing-module-docstring, too-few-public-methods
from data_access import ability_immunities
from utility_methods import get_two_types


def _generate_type_chart():
    """
    Generates the type chart for every type in Pokémon Xenoverse, which uses Gen V mechanics and the Sound type.

    The chart is a dictionary of dictionaries, with the outer dictionary containing the defending type and the inner
    dictionary containing the attacking type and the multiplier.

    :return dict[str, dict[str, int]]: A full type chart of defensive-first match ups.
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
    A class to calculate the defensive type matchups of a Pokémon given its (up to) two types, accounting for abilities
    that grant immunities and otherwise indicating extra information if some immunities are removed in the course of a
    battle.
    """
    def __init__(self, p_data):
        """
        The init function for TypeEffectivenessCalculator

        :param p_data: A dictionary containing all the Pokémon's data in pokemon.txt.
        """
        self.p_data = p_data
        self.first_type, self.second_type = get_two_types(p_data)

        self.abilities = p_data["Abilities"].split(",")
        if "HiddenAbility" in p_data:
            self.abilities.append(p_data["HiddenAbility"])

        # Indicates if a note box is needed
        self.notes = False

    def account_for_types(self, type_eff_box):
        """
        Appends extra information to the type effectiveness box to do with certain immunity-giving types.

        These types have immunities which are nullable through certain moves (e.g., Gravity against Flying) or
        abilities (e.g., Scrappy against Ghost), and their new match ups need to be taken into account.

        :param list[str] type_eff_box: The wiki code to produce the type effectiveness box.
        """
        # List of types with nullable immunities (e.g., by Scrappy, or Gravity, or Mind Reader)
        immune_types = ["Ghost", "Flying", "Dark"]
        types = [self.first_type, self.second_type]

        blank_type_chart = _generate_type_chart()

        for idx, i_type in enumerate(immune_types):
            if i_type in types:
                # Finds the other type for a dual-type Pokémon. If a single-type Pokémon, returns the same type.
                other_type = types[1 - types.index(i_type)].title()

                type_eff_box.append(f"|{i_type.lower()} = yes")

                if idx == 0:
                    # These if statements account for single-typed Pokémon, which have default weaknesses of 1x
                    if other_type == "Ghost":
                        new_normal = 1
                        new_fighting = 1
                    # Otherwise, finds the new match up as if the other type was reduced to 1x - e.g., a Fire/Flying
                    # Pokémon would be 2x weak to Ground under Gravity, because Fire's type chart is 2x weak to Ground.
                    else:
                        new_normal = blank_type_chart[other_type]["Normal"]
                        new_fighting = blank_type_chart[other_type]["Fighting"]
                    type_eff_box.append(f"|newnormal = {new_normal}")
                    type_eff_box.append(f"|newfighting = {new_fighting}")
                elif idx == 1:
                    if other_type == "Flying":
                        new_ground = 1
                    else:
                        new_ground = blank_type_chart[other_type]["Ground"]
                    type_eff_box.append(f"|newground = {new_ground}")
                else:
                    if other_type == "Dark":
                        new_psychic = 1
                    else:
                        new_psychic = blank_type_chart[other_type]["Psychic"]
                    type_eff_box.append(f"|newpsychic = {new_psychic}")

                self.notes = True

    def account_for_abilities(self, type_match_ups, type_eff_box):
        """
        Accounts for immunities or other changes to type match ups due to a Pokémon's ability.

        Note that some liberties are taken as all Pokémon's attributes are final in Xenoverse. So, for example, I know
        that no Pokémon has Dry Skin as its only ability, and can format appropriately without extra conditionals.

        :param dict[str, float] type_match_ups: A dictionary comprised of types and their relative multiplier.
        :param list[str] type_eff_box: The wiki code to produce the type effectiveness box.
        """
        # Some immune abilities are the sole ability of a Pokémon, and so are factored directly into the type
        # effectiveness box. Others are not, and so are marked as "maybe" in the box and not directly shown.
        sole_ability = "yes" if len(self.abilities) == 1 else "maybe"

        for ability in self.abilities:
            immune_type = ability_immunities(ability)
            if immune_type is not None:
                type_eff_box.append(f"|{ability.lower()} = {sole_ability}")
                if sole_ability == "yes":
                    type_eff_box.append(f"|new{immune_type.lower()} = {type_match_ups[immune_type]}")
                    type_match_ups[immune_type] = 0
                self.notes = True
            # Abilities more complex than granting a single immunity are accounted for here
            elif ability in ["DRYSKIN"]:
                type_eff_box.append(f"|{ability.lower()} = maybe")
                type_eff_box.append(f"|newfire = {type_match_ups["Fire"] * 1.25}")
                self.notes = True
            elif ability in ["HEATPROOF"]:
                type_eff_box.append(f"|{ability.lower()} = {sole_ability}")
                type_eff_box.append(f"|newfire = {type_match_ups["Fire"] * 0.5}")
                self.notes = True
            elif ability in ["MYSTICWIND"]:
                type_eff_box.append(f"|{ability.lower()} = yes")
                for a_type in ["Bug", "Dark", "Fighting"]:
                    type_eff_box.append(f"|new{a_type.lower()} = {type_match_ups[a_type]}")
                    type_match_ups[a_type] *= 0.5
                type_eff_box.append(f"|newdragon = {type_match_ups['Dragon']}")
                type_match_ups["Dragon"] = 0
                self.notes = True
            elif ability in ["FILTER", "SOLIDROCK"]:
                type_eff_box.append(f"|{ability.lower()} = maybe")
                for type_mu in type_match_ups.items():
                    if type_mu[1] > 1:
                        type_eff_box.append(f"|new{type_mu[0].lower()} = {type_mu[1] * 0.75}")
                self.notes = True
            elif ability in ["THICKFAT"]:
                type_eff_box.append(f"|{ability.lower()} = maybe")
                type_eff_box.append(f"|newfire = {type_match_ups["Fire"] * 0.5}")
                type_eff_box.append(f"|newice = {type_match_ups["Ice"] * 0.5}")
                self.notes = True

    def calculate_type_effectiveness(self):
        """
        Calculates the effectiveness of types against the Pokémon given its types and abilities.

        This is done by finding the multipliers of types against each of the Pokémon's types, and then multiplying them
        together to find the final multiplier, which is displayed in the hundreds in the wiki box. Also accounts for
        immunity granting abilities.

        :return dict[str, float]: A dictionary comprised of types and their relative multiplier.
        """
        type_chart = _generate_type_chart()

        # Retrieves the match up information for the first type
        first_match_ups = type_chart[self.first_type]

        # Dual typing may need to be taken into account
        if self.second_type != self.first_type:
            second_match_ups = type_chart[self.second_type]

            final_match_ups = {}
            for first_type_mu in first_match_ups.items():
                # if the second type does not affect a particular match up, just use the first type
                if first_type_mu[0] not in second_match_ups:
                    final_match_ups[first_type_mu[0]] = first_type_mu[1]
                else:
                    second_type_mu = second_match_ups[first_type_mu[0]]
                    final_match_ups[first_type_mu[0]] = first_type_mu[1] * second_type_mu

            return final_match_ups

        return first_match_ups

    def create_type_effectiveness(self):
        """
        Creates the type effectiveness box for the Pokémon wiki page.

        :return list[str]: The wiki code to produce the type effectiveness box.
        """
        type_eff_box = ["{{TypeEffectiveness", "|type1 = " + self.first_type]

        if self.second_type != self.first_type:
            type_eff_box.append("|type2 = " + self.second_type)

        type_match_ups = self.calculate_type_effectiveness()

        self.account_for_types(type_eff_box)
        self.account_for_abilities(type_match_ups, type_eff_box)

        # Accounts for non-neutral type match ups
        for type_name, multiplier in type_match_ups.items():
            if multiplier != 1:
                type_eff_box.append(f"|{type_name} = {int(multiplier * 100)}")

        if self.notes:
            type_eff_box.append("|notes = yes")

        type_eff_box.append("}}")

        return type_eff_box
