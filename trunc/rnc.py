# -*- coding: utf-8 -*-

"""
*********
trunc.rnc
*********

This module defines objects for interfacing with the Russian National Corpus.
"""

from __future__ import absolute_import, print_function

import re

class RNCSource(object):
    """One source in RNC search results.

    :param source_name: the full name of the source, as it appears inside the ``<span>`` element.
    :type source_name: ``str``, ``unicode``

    """

    def __init__(self, source_name):
        """Initialize the RNCSource object."""
        self.source_name = source_name
        # strip parentheses and their contents
        self.bare_name = re.sub(r'\([^)]*\)', '', self.source_name)
        # assign some default values to dates
        self.date_begin = 0.0
        self.date_middle = 0.0
        self.date_end = 0.0
        # parse the source string to find the dates
        self.parse_dates()

    def parse_dates(self):
        """Parse the source name and update the object's ``date`` attributes.

        If a source's name contains a date range, its ``date_middle`` is the
        average value of the two dates in the range:

        >>> a = RNCSource(u"И. Э. Кио. Иллюзии без иллюзий (1995-1999)")
        >>> a.date_begin, a.date_middle, a.date_end
        (1995.0, 1997.0, 1999,0)

        If a source's name contains only one date, all three ``date``
        attributes are identical:

        >>> b = RNCSource(u"В. Г. Распутин. Новая профессия (1998)")
        >>> b.date_begin, b.date_middle, b.date_end
        (1998.0, 1998.0, 1998.0)

        If a source contains multiple individual dates (but not a range), the
        earliest date is chosen, as this typically occurs when a source name
        describes a reprinted work, and both the original publication year
        and the reprinted publication year are provided:

        >>> c = RNCSource(u"Фридрих Горенштейн. Куча (1982) // «Октябрь», 1996")
        >>> c.date_begin, c.date_middle, c.date_end
        (1982.0, 1982.0, 1982.0)

        If a source contains no dates at all, the default date values of
        ``0.0`` are used. This is uncommon in the main (modern) corpus, but
        happens frequently in the historical corpora:

        >>> d = RNCSource(u"Житие Андрея Юродивого")
        >>> d.date_begin, d.date_middle, d.date_end
        (0.0, 0.0, 0.0)

        """
        date_seq = re.findall(r'\d{4}-\d{4}', self.source_name)
        if date_seq:
            self.date_begin = float(date_seq[0].split('-')[0])
            self.date_end = float(date_seq[0].split('-')[1])
            self.date_middle = (self.date_begin + self.date_end) / 2.0
        else:
            dates = re.findall(r'\d{4}', self.source_name)
            if dates:
                self.date_begin = float(min(dates))
                self.date_middle = float(min(dates))
                self.date_end = float(min(dates))
            else:
                pass
