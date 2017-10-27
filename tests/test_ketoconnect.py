import unittest

from scrapy import http

from scraper import ketoconnect


class KetoConnectParseTitleTest(unittest.TestCase):

    def test_scrapes_title_with_no_flavor_text(self):
        self.assertEqual(
            ketoconnect.parse_title(
                http.TextResponse(
                    url='',
                    body="""
<html>
<meta
  property="og:image"
  content="https://www.ketoconnect.net/recipe-image.jpg" />
<h1 class="entry-title">
  <a href="https://www.ketoconnect.net/recipe/keto-butter-chicken/">Keto Butter Chicken</a>
</h1>
</html>""")), 'Keto Butter Chicken')

    def test_scrapes_title_with_multiple_h1(self):
        self.assertEqual(
            ketoconnect.parse_title(
                http.TextResponse(
                    url='',
                    body="""
<h1 class="entry-title">
  <a href="https://www.ketoconnect.net/recipe/cooked-oven-meat/">Cooked Oven Meat</a>
</h1>
<h1>Non-title text</h1>""")), 'Cooked Oven Meat')

    def test_scrapes_title_and_removes_flavor_text(self):
        self.assertEqual(
            ketoconnect.parse_title(
                http.TextResponse(
                    url='',
                    body="""
<html>
<h1 class="entry-title">
  <a href="https://www.ketoconnect.net/recipe/cauliflower-waffles/">Cauliflower Waffles | Bacon and Cheddar!</a>
</h1>
</html>""")), 'Cauliflower Waffles')
