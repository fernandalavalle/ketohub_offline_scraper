import unittest

from scrapy import http

from scraper import keto_size_me
from scraper.common import errors


class KetoSizeMeParseCategoryTest(unittest.TestCase):

    def test_when_meta_section_does_not_specify_category_raises_exception(self):
        with self.assertRaises(errors.NoRecipeFoundError):
            keto_size_me.scrape_category(
                http.TextResponse(
                    url='https://ketosizeme.com/keto-bulletproof-coffee/',
                    body="""
<meta property="article:section" content="Keto Brands We Love" />
"""))
