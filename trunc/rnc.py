# -*- coding: utf-8 -*-

"""
*********
trunc.rnc
*********

This module defines classes for interfacing with the Russian National Corpus.

Those classes fall broadly into two types: *queries* and *elements*.

* Queries are derived from the :class:`RNCQueryGeneric` class and describe
  a particular seach of one corpus.
* Elements are derived from the :class:`RNCElementGeneric` class and each
  describe a level in the hierarchy of units which result from a query.

"""

from __future__ import absolute_import, print_function

from bs4 import BeautifulSoup as Soup
import re
import urllib

from .util import as_integer, to_unicode_or_bust
from .web import Webpage

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

    def __unicode__(self):
        """Return a human-readable unicode representation of the RNCSource.

        :rtype: ``unicode``
        """
        return u'RNC Source: {}'.format(self.source_name)

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


class RNCQueryGeneric(object):
    """Generic query of the Russian National Corpus.

    The :class:`RNCQueryGeneric` class defines a generic query of the Russian
    National Corpus. The more specific queries :class:`RNCQueryOld`,
    :class:`RNCQueryMid`, and :class:`RNCQueryMain` all inherit from this
    base class.

    The keyword arguments ``**kwargs`` passed to the class at initialization
    represent the key-value pairs used to assemble a complete search URL. For
    example, searching the main corpus of the RNC for the verb lemma
    *учитать* (using the online interface) generates the following URL:

        http://search.ruscorpora.ru/search.xml?mycorp=&mysent=&mysize=&dpp=&
        spp=&spd=&text=lexgramm&mode=main&sort=gr_tagging&lang=en&parent1=0&
        level1=0&lex1=%F3%F7%E8%F2%E0%F2%FC&gramm1=&sem1=&flags1=&
        sem-mod1=sem&sem-mod1=sem2&parent2=0&level2=0&min2=1&max2=1&lex2=&
        gramm2=&sem2=&flags2=&sem-mod2=sem

    The key-value pair ``mode=main`` is one pair which would need to be
    provided at initialization in order to produce the above URL. The
    following example constructs the query described by the above URL using
    provided key-value pairs:

        >>> q = RNCQueryGeneric(
                mycorp='', mysent='', mysize='', dpp='', spp='', spd='',
                text='lexgramm', mode='main', sort='gr_tagging', lang='en',
                parent1=0, level1=0, lex1='%F3%F7%E8%F2%E0%F2%FC', gramm1='',
                sem1='', flags1='', sem_mod1='sem', parent2=0, level2=0,
                min2=1, max2=1, lex2='', gramm2='', sem2='', flags2='',
                sem_mod2='sem'
                )
        >>> print(q.url())
        http://search.ruscorpora.ru/search.xml?spp=&text=lexgramm&mysent=&
        level1=0&level2=0&spd=&flags1=&mysize=&sem_mod1=sem&sem_mod2=sem&
        sem2=&sem1=&mode=main&sort=gr_tagging&gramm1=&gramm2=&min2=1&lang=en&
        lex1=%F3%F7%E8%F2%E0%F2%FC&lex2=&max2=1&flags2=&mycorp=&parent2=0&
        parent1=0&dpp=&

    Note that any keys containing a hyphen (e.g., ``sem-mod1``) should be
    passed to the class call with an underscore instead so that they are
    valid Python identifiers (e.g., ``sem_mod1``). They're converted back
    into hyphens by the class's :func:`url` method.

    Note also that not all of the key-value pairs need to be called explicitly
    when a new object of the class is created. Many of them are defaults and
    will be supplied automatically.

    """

    DEFAULTS = {
        'mode': '',
        }

    def __init__(self, url=None, **kwargs):
        """Initialize the RNCQueryGeneric object.

        The :class:`RNCQueryGeneric` class, as well as its subclasses
        :class:`RNCQueryOld`, :class:`RNCQueryMid`, and :class:`RNCQueryMain`,
        has a class variable ``DEFAULTS``. This is a dictionary in which each
        key is a parameter and each value is the corresponding value of that
        parameter.

        At initialization, key-value pairs from this ``DEFAULTS`` dictionary
        are used to populate the attributes of the instance with any
        necessary parameters which were not specified explitictly.

        :param url: actual URL of a RNC search
        :type url: ``str``
        :param kwargs: keyword arguments representing parameters and values
        """
        self.base_url = "http://search.ruscorpora.ru/search.xml?"
        if url is not None:
            self.parse_url(url)
        else:
            if kwargs:
                for k, v in kwargs.iteritems():
                    a = getattr(self, k, None)
                    if a is None:
                        setattr(self, k, v)
            for k, v in self.__class__.DEFAULTS.iteritems():
                a = getattr(self, k, None)
                if a is None:
                    setattr(self, k, v)

    def parse_url(self, url):
        """Parse a supplied query URL to update instance attributes.

        This method splits a provided URL into its constituent parts and
        uses those parts to update the instance variables of the RNCQuery
        object. This allows for an existing query URL (generated by using
        the RNC's standard web interface, for instance) to be copied/pasted
        rather than typed out parameter by parameter.

        :param url: complete URL representing a query of the RNC
        :type url: ``str``
        """
        w = Webpage(url)
        enc = w.soup().original_encoding
        url_halves = url.split('?', 1)
        params = url_halves[1].split('&')
        for param in params:
            kv = param.split('=')
            k = kv[0].replace('-', '_')
            v = kv[1]
            if '%' in v:
                v = urllib.unquote(v).decode(enc)
                v = to_unicode_or_bust(v)
            elif v.isdigit():
                v = as_integer(v)

            # set all attributes except for the page index
            if k != 'p':
                setattr(self, k, v)

        self.base_url = url_halves[0] + '?'


    def url(self):
        """Return the url for a search of the Russian National Corpus.

        :rtype: ``str``
        """
        address = self.base_url
        for k, v in self.__dict__.iteritems():
            if k != 'base_url':
                k = k.replace('_', '-')
                if k == 'lex1':
                    v = urllib.quote(to_unicode_or_bust(v).encode('utf-8'))
                address += "{}={}&".format(k, v)
        return address

    def documents_and_contexts(self, url=None):
        """Return a 2-tuple representing the number of query results.

        This method.

            >>> b = RNCQueryMain(lex1="учитать")
            >>> rb = b.documents_and_contexts()
            >>> print(rb)
            (3, 3)
            >>> c = RNCQueryMain(lex1="читать")
            >>> rc = c.documents_and_contexts()
            >>> print(rc)
            (14311, 89547)

        :param url: address of the query to search for
        :type url: ``str``
        :returns: a tuple of two integers, of which the first represents the number of documents and the second represents the number of contexts (tokens)
        :rtype: ``tuple``
        """
        if url is None:
            url = self.url()
        page = Webpage(url)
        d_selector = "body > div.content > p.found > span:nth-of-type(1)"
        c_selector = "body > div.content > p.found > span:nth-of-type(3)"
        d = page.soup().select(d_selector)[0].text
        c = page.soup().select(c_selector)[0].text

        return (as_integer(d), as_integer(c))


class RNCQueryOld(RNCQueryGeneric):
    """Query of the Old subcorpus of the Russian National Corpus."""

    DEFAULTS = {
        'mode': 'old_rus',
        'text1': 'lexgramm',
        'doc_docid': '0|13|2|3|1|4|7|8|10|12|5|11|9|6',
        'parent1': 0,
        'level1': 0,
        'lexi1': '',
        'gramm1': '',
        'parent2': 0,
        'level2': 0,
        'min2': 1,
        'max2': 1,
        }

    def __init__(self, **kwargs):
        """Initialize the RNCQueryOld object."""
        super(self.__class__, self).__init__(**kwargs)
        self.base_url = "http://search-beta.ruscorpora.ru/search.xml?"


class RNCQueryMid(RNCQueryGeneric):
    """Query of the Mid subcorpus of the Russian National Corpus."""

    DEFAULTS = {
        'env': 'alpha',
        'mode': 'mid_rus',
        'text': 'lexform',
        'sort': 'gr_created',
        'lang': 'ru',
        'mycorp': '',
        'mysent': '',
        'mysize': '',
        'mysentsize': '',
        'mydocsize': '',
        'dpp': '',
        'spp': '',
        'spd': '',
        'req': '',
        }

    def __init__(self, **kwargs):
        """Initialize the RNCQueryMid object."""
        super(self.__class__, self).__init__(**kwargs)
        self.base_url = "http://search-beta.ruscorpora.ru/search.xml?"


class RNCQueryMain(RNCQueryGeneric):
    """Query of the Main subcorpus of the Russian National Corpus."""

    DEFAULTS = {
        'mycorp': '',
        'mysent': '',
        'mysize': '',
        'dpp': '',
        'spp': '',
        'spd': '',
        'text': 'lexgramm',
        'mode': 'main',
        'sort': 'gr_tagging',
        'lang': 'en',
        'parent1': 0,
        'level1': 0,
        'lex1': '',
        'gramm1': '',
        'sem1': '',
        'flags1': '',
        'sem-mod1': '',
        'sem-mod2': '',
        'parent2': 0,
        'level2': 0,
        'min2': 1,
        'max2': 1,
        'lex2': '',
        'gramm2': '',
        'sem2': '',
        'flags2': '',
        }

    def __init__(self, url=None, **kwargs):
        """Initialize the RNCQueryMain object."""
        self.base_url = "http://search.ruscorpora.ru/search.xml?"
        super(self.__class__, self).__init__(url=url, **kwargs)


class RNCResultGeneric(object):
    """Generic element in the results of a query of the RNC."""

    def __init__(self, **kwargs):
        """Initialize the RNCResultGeneric object."""
        if kwargs:
            if 'root' in kwargs:
                root = kwargs['root']
                tags = ["<class 'bs4.element.Tag'>",
                        "<class 'bs4.BeautifulSoup'>"]
                if str(type(root)) not in tags:
                    self.root = soup(root)
                else:
                    self.root = root
            if 'url' in kwargs:
                url = kwargs['url']
                self.root = Webpage(url).soup()


class RNCResultPage(RNCResultGeneric):
    """One page in RNC search results."""

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

    def page_result_list(self):
        return self.root.find(
                'p', class_='pager').find_next_sibling('ol').contents

    def __iter__(self):
        return iter(self.page_result_list())

    def __getitem__(self, idx):
        return self.page_result_list()[idx]

    def __len__(self):
        return len(self.page_result_list())


class RNCResultContext(RNCResultGeneric):
    """One entry in a RNCResultsPage.page_results_list list."""

    def __init__(self, **kwargs):
        super(self.__class__, self).__init__(**kwargs)

        self.source = RNCSource(self.root.contents[0].string)

    def words(self):
        pass
