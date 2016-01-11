# -*- coding: utf-8 -*-

"""Provides classes for accessing web pages."""

from __future__ import absolute_import, print_function

import time

from bs4 import BeautifulSoup as Soup
from urllib import FancyURLopener

from .util import fibonacci_number

class MyOpener(FancyURLopener):
    """A FancyURLopener object with a custom User-Agent field."""

    version = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) "
               "AppleWebKit/600.5.17 (KHTML, like Gecko) "
               "Version/8.0.5 Safari/600.5.17")

class Webpage(object):
    """Generic webpage with attributes."""

    def __init__(self, address, delay=1):
        """Initialize the Webpage object.

        :param address: url of the webpage
        :param delay: ideal delay interval, in seconds, between page loads
        (default is ``1``)
        """
        self.address = address
        self.opener = MyOpener()
        self.delay = delay

    def open(self):
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
                self.page = self.opener.open(self.address)
                page_not_loaded = False
            except IOError as e:
                print("\nIOError: {}\nat {}".format(e, self.address))
                time.sleep(fibonacci_number(attempt))
                attempt += 1

        return self.page

    def html(self):
        """Return contents of the Webpage as html."""
        return self.open().read()

    def soup(self):
        """Return contents of the Webpage as a BeautifulSoup object."""
        return Soup(self.html())
