#!/usr/bin/env python3

from hypothesis import assume, given
import pytest
import trunc.util as util

from .generate import String


@given(String.OF_DIGITS)
def test_getting_digits_from_strings_of_all_digits(s):
    assert s == util.just_digits(s)


@given(String.NO_DIGITS)
def test_getting_digits_from_nonempty_strings_with_no_digits(s):
    assert '' == util.just_digits(s)


@given(String.OF_DIGITS)
def test_converting_strings_that_contain_all_numbers(s):
    assert int(s) == util.ints_from_string(s)


@given(String.OF_DIGITS_AND_WHITESPACE)
def test_converting_strings_that_contain_numbers_and_spaces(s):
    assume("" != s.strip())
    assert isinstance(util.ints_from_string(s), int)


@given(String.NO_DIGITS)
def test_converting_nonempty_strings_with_no_digits(s):
    with pytest.raises(ValueError):
        util.ints_from_string(s)
