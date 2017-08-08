#!/usr/bin/env python3

import pytest
import trunc.util as util


def test_getting_digits_from_strings_of_all_digits():
    assert '123' == util.just_digits('123')
    assert '1' == util.just_digits('1')


def test_getting_digits_from_nonempty_strings_with_no_digits():
    assert '' == util.just_digits('abcde')
    assert '' == util.just_digits('./+')


def test_converting_strings_that_contain_all_numbers():
    assert 123 == util.ints_from_string('123')
    assert 12345 == util.ints_from_string('12345')


def test_converting_strings_that_contain_numbers_and_spaces():
    assert 14311 == util.ints_from_string('14 311')
    assert 12345 == util.ints_from_string('12 345')


def test_converting_nonempty_strings_with_no_digits():
    with pytest.raises(ValueError):
        util.ints_from_string('abc')
