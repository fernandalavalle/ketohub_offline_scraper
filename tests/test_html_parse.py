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


class ScrapeRuledMeHtml(unittest.TestCase):

    def test_scrapes_title_and_simple_category(self):
        self.assertEqual(
            html_parse.parse('https://www.ruled.me/keto-beef-wellington/', """
<html>
<h1>Keto Beef Wellington</h1>
<div class="postCategories">
&gt; <a rel="nofollow" href="" title="Dinner">Dinner</a>
</div>
</html>"""), {
                'title': 'Keto Beef Wellington',
                'url': 'https://www.ruled.me/keto-beef-wellington/',
                'category': 'entree',
            })

    def test_scrapes_title_and_hierarchical_category(self):
        self.assertEqual(
            html_parse.parse('https://www.ruled.me/keto-sushi/', """
<html>
<h1>Keto Sushi</h1>
<div class="postCategories">
Keto Recipes &gt; <a rel="nofollow" href="https://www.ruled.me/keto-recipes/" title="Dinner">Dinner</a>
</div>
</html>"""), {
                'title': 'Keto Sushi',
                'url': 'https://www.ruled.me/keto-sushi/',
                'category': 'entree',
            })

    def test_scrapes_title_and_reverse_hierarchical_category(self):
        self.assertEqual(
            html_parse.parse('https://www.ruled.me/cauliflower-mac-cheese/', """
<html>
<h1>Cauliflower Mac & Cheese</h1>
<div class="postCategories">
Side Items &gt; <a rel="nofollow" href="https://www.ruled.me/keto-recipes/side-items/" title="Keto Recipes">Keto Recipes</a>
</div>
</html>"""), {
                'title': 'Cauliflower Mac & Cheese',
                'url': 'https://www.ruled.me/cauliflower-mac-cheese/',
                'category': 'side',
            })