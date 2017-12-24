import unittest

from scrapy import http

from scraper import low_carb_yum


class LowCarbYumParseTitleTest(unittest.TestCase):

    def test_strips_tags_after_pipe(self):
        self.assertEqual(
            low_carb_yum.scrape_title(
                http.TextResponse(
                    url='',
                    body="""
<meta property="og:title" content="Almond Flour Biscuits - Paleo Low Carb" />"""
                )), 'Almond Flour Biscuits')
