#!/usr/bin/env python3

from hypothesis import strategies as st
import string

non_digits = (c for c in string.printable if c not in string.digits)


class String:
    OF_DIGITS = st.text(alphabet=list(string.digits), min_size=1)

    NO_DIGITS = st.text(alphabet=list(non_digits), min_size=1)

    OF_DIGITS_AND_WHITESPACE = st.text(
        alphabet=list(c for c in (string.digits + string.whitespace)),
        min_size=1)

    @classmethod
    def OF(cls, letters):
        return st.text(alphabet=list(letters), min_size=1)

    @classmethod
    def OF_DIGITS_AND(cls, others):
        chars = list(string.digits) + list(c for c in others)
        return st.text(alphabet=chars, min_size=1)
