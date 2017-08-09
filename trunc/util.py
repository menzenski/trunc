#!/usr/bin/env python3

import re


def just_digits(string_with_nums: str) -> int:
    """
    Return the input string with all non-digit characters removed.
    """
    return re.sub(r'[^\d]+', '', string_with_nums)


def ints_from_string(string_with_nums: str) -> int:
    """
    Remove all non-digit characters from a string and return its integer value.
    """
    return int(just_digits(string_with_nums))
