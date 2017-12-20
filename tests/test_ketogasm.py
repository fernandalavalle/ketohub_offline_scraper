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
<h1 class="entry-title">Low Carb Moscow Mule &#8211; [Keto, Alcohol, Sugar Free]</h1>"""
                )), 'Low Carb Moscow Mule')

    def test_strips_tags_after_pipe(self):
        self.assertEqual(
            ketogasm.parse_title(
                http.TextResponse(
                    url='',
                    body="""
<h1 class="entry-title">Spanish Cauliflower Rice | Low Carb</h1>""")),
            'Spanish Cauliflower Rice')

    def test_strips_tags_after_colon(self):
        self.assertEqual(
            ketogasm.parse_title(
                http.TextResponse(
                    url='',
                    body="""
<h1 class="entry-title">Vodka Mojito: Low Carb and Sugar-Free</h1>""")),
            'Vodka Mojito')
        self.assertEqual(
            ketogasm.parse_title(
                http.TextResponse(
                    url='',
                    body="""
<h1 class="entry-title">Hot Buttered Rum Recipe: Low Carb, Sugar Free</h1>""")),
            'Hot Buttered Rum Recipe')
        self.assertEqual(
            ketogasm.parse_title(
                http.TextResponse(
                    url='',
                    body="""
<h1 class="entry-title">Gin Fizz Cocktail Recipe &#8211; Low Carb &#038; Sugar Free!</h1>
""")), 'Gin Fizz Cocktail Recipe')

    def test_strips_tags_after_dash(self):
        self.assertEqual(
            ketogasm.parse_title(
                http.TextResponse(
                    url='',
                    body="""
<h1 class="entry-title">Spicy Chicken Sausage &#x2013; Low Carb, Gluten-Free</h1>"""
                )), u'Spicy Chicken Sausage')

    def test_keeps_non_tag_text_after_dash(self):
        self.assertEqual(
            ketogasm.parse_title(
                http.TextResponse(
                    url='',
                    body="""
<h1 class="entry-title">Pumpkin Seed Bark &#x2013; Dark Chocolate and Sea Salt</h1>"""
                )), u'Pumpkin Seed Bark \u2013 Dark Chocolate and Sea Salt')

        self.assertEqual(
            ketogasm.parse_title(
                http.TextResponse(
                    url='',
                    body="""
<h1 class="entry-title">Keto Flatbread Recipe &#x2013; Low Carb, Gluten Free</h1>"""
                )), u'Keto Flatbread Recipe')


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
