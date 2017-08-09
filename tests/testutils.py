#!/usr/bin/env python3

from hypothesis import strategies as st
import string

non_digits = (c for c in string.printable if c not in string.digits)


class Generators:
    STRING_OF_DIGITS = st.text(alphabet=list(string.digits), min_size=1)

    STRING_NO_DIGITS = st.text(alphabet=list(non_digits), min_size=1)

    STRING_OF_DIGITS_AND_WHITESPACE = st.text(
        alphabet=list(c for c in (string.digits + string.whitespace)),
        min_size=1)

    @classmethod
    def STRING_OF(cls, letters):
        return st.text(alphabet=list(letters), min_size=1)

    @classmethod
    def STRING_OF_DIGITS_AND(cls, others):
        chars = list(string.digits) + list(c for c in others)
        return st.text(alphabet=chars, min_size=1)
