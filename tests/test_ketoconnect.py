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
<h1 class="entry-title">
  <a href="https://www.ketoconnect.net/recipe/keto-butter-chicken/">Keto Butter Chicken</a>
</h1>""")), 'Keto Butter Chicken')

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
<h1 class="entry-title">
  <a href="https://www.ketoconnect.net/recipe/cauliflower-waffles/">Cauliflower Waffles | Bacon and Cheddar!</a>
</h1>""")), 'Cauliflower Waffles')


class KetoConnectParseCategoryTest(unittest.TestCase):

    def test_scrapes_non_opengraph_image(self):
        self.assertEqual(
            ketoconnect.parse_category(
                http.TextResponse(url='', body=''), {
                    'referer': 'https://www.ketoconnect.net/main-dishes/',
                }), 'entree')


class KetoConnectParseImageTest(unittest.TestCase):

    def test_scrapes_opengraph_image(self):
        self.assertEqual(
            ketoconnect.parse_image(
                http.TextResponse(
                    url='',
                    body="""
<meta
  property="og:image"
  content="https://www.ketoconnect.net/recipe-image.jpg" />
""")), 'https://www.ketoconnect.net/recipe-image.jpg')

    def test_scrapes_non_opengraph_image(self):
        self.assertEqual(
            ketoconnect.parse_image(
                http.TextResponse(
                    url='',
                    body="""
<div id="tve_editor">
<span class="junk">
<img class="tve_image" alt="" style="width: 400px;" src="https://www.ketoconnect.net/recipe-image.jpg" width="400" height="600" data-attachment-id="9282">
</span>
</div>""")), 'https://www.ketoconnect.net/recipe-image.jpg')
