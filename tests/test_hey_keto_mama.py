import unittest

from scrapy import http

from scraper import hey_keto_mama


class HeyKetoMamaParseTitleTest(unittest.TestCase):

    def test_strips_trailing_page_title(self):
        self.assertEqual(
            hey_keto_mama.scrape_title(
                http.TextResponse(
                    url='',
                    body="""
<meta property="og:title" content="Cream Cheese &amp; Salami Keto Pinwheels - Hey Keto Mama" />"""
                )), u'Cream Cheese & Salami Keto Pinwheels')
