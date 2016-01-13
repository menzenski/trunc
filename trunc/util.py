# -*- coding: utf-8 -*-

"""
**********
trunc.util
**********

This module provides miscellaneous helpful utility functions."""

from __future__ import absolute_import, print_function

def fibonacci_number(n):
    """Return the nth number in the Fibonacci series.

    Each number in the Fibonacci series is equal to the sum of the
    preceding two numbers:

        1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ...

    :param n: The position in the Fibonacci series whose value will be returned
    :rtype: ``int``

    >>> fibonacci_number(6)
    8

    """
    a, b = 1, 1
    for _ in xrange(n - 1):
        a, b = b, a + b
    return a

def to_unicode_or_bust(obj, encoding='utf-8'):
    """Return ``obj`` as ``unicode``.

    Credit for this function belongs to
    `Kumar McMillan <http://farmdev.com/talks/unicode>`_.

    :param obj: the object to be returned as ``unicode``
    :type obj: ``str``, ``unicode``
    :param encoding: the desired encoding (UTF-8 is the default)
    :rtype: ``unicode``
    """
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj


