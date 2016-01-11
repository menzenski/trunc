# -*- coding: utf-8 -*-

"""Provides utilities for handling unicode and saving output."""

from __future__ import absolute_import, print_function

def fibonacci_number(n):
    """Return the nth Fibonacci number.

    :param n: The position to be returned in the Fibonacci series
    :rtype: ``int``
    """
    a, b = 1, 1
    for _ in xrange(n - 1):
        a, b = b, a + b
    return a

def to_unicode_or_bust(obj, encoding='utf-8'):
    """Return ``obj`` as ``unicode``.

    Credit for this function belongs to
    `Kumar McMillan <http://farmdev.com/talks/unicode>`.

    :param obj: the object to be returned as ``unicode``
    :type obj: ``str``, ``unicode``
    :param encoding: the desired encoding (UTF-8 is the default)
    :rtype: ``unicode``
    """
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj


