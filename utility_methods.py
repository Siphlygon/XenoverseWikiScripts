# pylint: disable=locally-disabled, too-many-lines, line-too-long
"""
Contains methods used in multiple modules to provide extra utility.
"""


def make_three_digits(digits):
    """
    Converts a string of digits, specifically dex numbers, to a 3-digit string.

    :param str digits: The digits in the form of a string.
    :return str: The given string in 3-digit form.
    """
    # If a 3-digit number is already passed to this function, just return
    if len(digits) == 3:
        return digits

    # Accounts for Alolan/other forms of form "XXX_1" or w/e.
    # The extra "_1" is ignored --> wiki pages never use them
    curr_digits = digits.split("_")[0] if "_" in digits else digits

    # Add 0s as necessary to make it 3 digits:
    new_digits = "0" * (3 - len(curr_digits)) + curr_digits

    return new_digits


def find_dex_number(regional_numbers):
    """
    Takes regional numbers from pokemon.txt and converts into a Pokédex number of e.g., "X031".

    :param str regional_numbers: The regional numbers for a Pokémon in pokemon.txt.
    :return str: The (global) dex number for the Pokémon.
    """
    dex_parts = regional_numbers.split(",")

    # Regional numbers are in form "X,Y,Z", where X is normal dex, Y is xeno dex, Z is vintage dex
    # Every Pokémon only has 1 non-zero regional number
    if dex_parts[0] != "0":
        dex_nums = make_three_digits(dex_parts[0])
    elif dex_parts[1] != "0":
        # For some reason, X030 just doesn't exist in the game's data. As Pokédex numbers are only used for wiki display
        # anyway, I'm just going to manually adjust these numbers and keep w/ the X030 = Mewtwo X wiki system
        dex_num = int(dex_parts[1])
        dex_nums = f"X{make_three_digits(str(dex_num - 1))}" if dex_num > 29 else f"X{make_three_digits(dex_parts[1])}"
    else:
        dex_nums = f"V{make_three_digits(dex_parts[2])}"

    return dex_nums
