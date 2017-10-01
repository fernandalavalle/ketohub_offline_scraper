import unittest

from scraper import html_parse


class ScrapeKetoConnectHtml(unittest.TestCase):

    def test_scrapes_title_with_no_flavor_text(self):
        self.assertEqual(
            html_parse.parse(
                'https://www.ketoconnect.net/recipe/keto-butter-chicken/', """
<html>
<h1 class="entry-title">
  <a href="https://www.ketoconnect.net/recipe/keto-butter-chicken/">Keto Butter Chicken</a>
</h1>
</html>"""), {
                    'title': 'Keto Butter Chicken',
                    'url':
                    'https://www.ketoconnect.net/recipe/keto-butter-chicken/',
                    'category': 'entree',
                })

    def test_scrapes_title_and_removes_flavor_text(self):
        self.assertEqual(
            html_parse.parse(
                'https://www.ketoconnect.net/recipe/cauliflower-waffles/', """
<html>
<h1 class="entry-title">
  <a href="https://www.ketoconnect.net/recipe/cauliflower-waffles/">Cauliflower Waffles | Bacon and Cheddar!</a>
</h1>
</html>"""), {
                    'title': 'Cauliflower Waffles',
                    'url':
                    'https://www.ketoconnect.net/recipe/cauliflower-waffles/',
                    'category': 'entree',
                })
