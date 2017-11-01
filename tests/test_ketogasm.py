import unittest

from scrapy import http

from scraper import ketogasm


class KetogasmParseTitleTest(unittest.TestCase):

    def test_strips_bracketed_text(self):
        self.assertEqual(
            ketogasm.parse_title(
                http.TextResponse(
                    url='',
                    body="""
<h1 class="entry-title">Low Carb Moscow Mule Recipe &#8211; [Keto, Alcohol, Sugar Free]</h1>"""
                )), 'Low Carb Moscow Mule Recipe')


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
