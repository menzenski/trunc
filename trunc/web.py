# -*- coding: utf-8 -*-

"""
*********
trunc.web
*********

This module provides classes for accessing web pages."""

from __future__ import absolute_import, print_function

import codecs
import time

from bs4 import BeautifulSoup as Soup
from urllib import FancyURLopener

from .util import fibonacci_number

class MyOpener(FancyURLopener):
    """A FancyURLopener object with a custom User-Agent field.

    The ``MyOpener.version`` class attribute contains the User-Agent field.
    Use ``MyOpener.set_version()`` to change this attribute.
    """

    version = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) "
               "AppleWebKit/600.5.17 (KHTML, like Gecko) "
               "Version/8.0.5 Safari/600.5.17")

    def set_version(self, new_version):
        """Define a new User-Agent field for the MyOpener class.

        :param new_version: desired User-Agent field
        :type new_version: ``str``
        """
        MyOpener.version = new_version

class Webpage(object):
    """Generic webpage with attributes."""

    def __init__(self, address, delay=1, encoding='windows-1251'):
        """Initialize the Webpage object.

        :param address: url of the webpage
        :param delay: ideal delay interval, in seconds, between page loads
        (default is ``1``)
        :param encoding: encoding of the webpage
        """
        self.address = address
        self.opener = MyOpener()
        self.delay = delay
        self.encoding = encoding

    def page(self):
        """Open the webpage.

        If there's an error opening the page (i.e., if the Corpus throttles
        the scraper), wait and retry in successively longer intervals (which
        increase according to the Fibonacci sequence) until the page loads
        successfully.

        :rtype: ``<'instance'>``
        """
        attempt = 1
        page_not_loaded = True
        while page_not_loaded:
            try:
                time.sleep(self.delay)
                self.page_instance = self.opener.open(self.address)
                page_not_loaded = False
            except IOError as e:
                print("\nIOError: {}\nat {}".format(e, self.address))
                time.sleep(fibonacci_number(attempt))
                attempt += 1

        return self.page_instance

    def html(self, encoding=None):
        """Return contents of the Webpage as html."""
        if encoding is None:
            encoding = self.encoding
        return self.page().read().decode(encoding)

    def soup(self):
        """Return contents of the Webpage as a BeautifulSoup object."""
        return Soup(self.html())
