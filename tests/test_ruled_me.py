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


class RuledMeParseCategoryTest(unittest.TestCase):

    def test_scrapes_simple_category(self):
        self.assertEqual(
            ruled_me.parse_category(
                http.TextResponse(
                    url='',
                    body="""
<div class="postCategories">
&gt; <a rel="nofollow" href="" title="Dinner">Dinner</a>
</div>""")), 'entree')

    def test_scrapes_hierarchical_category(self):
        self.assertEqual(
            ruled_me.parse_category(
                http.TextResponse(
                    url='',
                    body="""
<div class="postCategories">
Keto Recipes &gt; <a rel="nofollow" href="https://www.ruled.me/keto-recipes/" title="Dinner">Dinner</a>
</div>""")), 'entree')

    def test_scrapes_reverse_hierarchical_category(self):
        self.assertEqual(
            ruled_me.parse_category(
                http.TextResponse(
                    url='',
                    body="""
<html>
<h1>Cauliflower Mac & Cheese</h1>
<div class="postCategories">
Side Items &gt; <a rel="nofollow" href="https://www.ruled.me/keto-recipes/side-items/" title="Keto Recipes">Keto Recipes</a>
</div>
</html>""")), 'side')
