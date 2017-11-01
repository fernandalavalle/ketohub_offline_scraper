import unittest

from scrapy import http

from scraper import ketogasm


class KetogasmParseCategoryTest(unittest.TestCase):

    def test_reads_none_category_when_category_not_defined(self):
        self.assertEqual(
            ketogasm.parse_category(
                http.TextResponse(
                    url='',
                    body="""
<script type="application/ld+json">
{
   "@context":"http:\/\/schema.org\/",
   "@type":"Recipe",
   "name":"Roasted Pumpkin Seeds Recipe"
}""")), None)
