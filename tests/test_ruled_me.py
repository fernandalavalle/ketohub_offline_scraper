import unittest

from scrapy import http

from scraper import ruled_me


class RuledMeParseTitleTest(unittest.TestCase):

    def test_scrapes_title_with_no_flavor_text(self):
        self.assertEqual(
            ruled_me.parse_title(
                http.TextResponse(
                    url='', body="""
<h1>Keto Beef Wellington</h1>
""")), 'Keto Beef Wellington')
