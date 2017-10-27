import os
import unittest

from scraper import html_parse


def _read_test_file(filename):
    basepath = os.path.dirname(__file__)
    filepath = os.path.join(basepath, 'testdata', filename)
    return open(filepath).read()


class ScrapeKetoConnectHtml(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_scrapes_ingredients(self):
        self.assertEqual(
            html_parse.parse({
                'url':
                'https://www.ketoconnect.net/recipe/low-carb-pizza-crust/',
                'referer':
                'https://www.ketoconnect.net/main-dishes/',
            }, _read_test_file('low-carb-pizza-crust.html')), {
                'title':
                'Low Carb Pizza Crust',
                'url':
                'https://www.ketoconnect.net/recipe/low-carb-pizza-crust/',
                'category':
                'entree',
                'ingredients': [
                    'Coconut flour',
                    'psyilium husk powder',
                    'active dry yeast',
                    'Baking powder',
                    'salt',
                    'olive oil',
                    'Water',
                    'eggs',
                    'minced garlic',
                    'Red Pepper Flakes',
                    'dried minced onion flakes',
                    'Oregano',
                ],
                'mainImage':
                'https://ketoconnect-apjirmx5iktkd7.netdna-ssl.com/wp-content/uploads/2017/10/low-carb-pizza-crust-slice-flat.jpg',
            })


class ScrapeRuledMeHtml(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_scrapes_ingredients(self):
        self.assertEqual(
            html_parse.parse({
                'url': 'https://www.ruled.me/keto-beef-wellington/'
            }, """
<html>
<h1>Keto Beef Wellington</h1>
<div class="postCategories">
&gt; <a rel="nofollow" href="" title="Dinner">Dinner</a>
</div>
<table>
<tbody>
<tr class="aad">
<td class="aae" height="17"><strong>Tropical Chocolate Mousse Bites</strong></td>
<td class="aac"><strong>Calories</strong></td>
<td class="aac"><strong>Fats(g)</strong></td>
<td class="aac"><strong>Carbs(g)</strong></td>
<td class="aac"><strong>Fiber(g)</strong></td>
<td class="aac"><strong>Net Carbs(g)</strong></td>
<td class="aac"><strong>Protein(g)</strong></td>
</tr>
<tr class="aad">
<td class="aad" height="17"><strong>10.5 ounces (300 g) sugar-free dark chocolate</strong></td>
<td align="right">1387</td>
<td align="right">89</td>
<td align="right">8</td>
<td align="right">0</td>
<td align="right">8</td>
<td align="right">20</td>
</tr>
<tr class="aad">
<td class="aad" height="17"><strong>1 ounce (30 g) coconut oil</strong></td>
<td align="right">268</td>
<td align="right">29.72</td>
<td align="right">0</td>
<td align="right">0</td>
<td align="right">0</td>
<td align="right">0</td>
</tr>
<tr class="aad">
<td class="aad" height="17"><strong>1/2 cup heavy whipping cream</strong></td>
<td align="right">405</td>
<td align="right">42.94</td>
<td align="right">3.26</td>
<td align="right">0</td>
<td align="right">3.26</td>
<td align="right">3.38</td>
</tr>
<tr class="aad">
<td class="aad" height="17"><strong>1 tablespoon lemon zest</strong></td>
<td align="right">3</td>
<td align="right">0.02</td>
<td align="right">0.96</td>
<td align="right">0.6</td>
<td align="right">0.36</td>
<td align="right">0.09</td>
</tr>
<tr class="aad">
<td class="aad" height="17"><strong>1 tablespoon shredded coconut</strong></td>
<td align="right">33</td>
<td align="right">3.33</td>
<td align="right">1.33</td>
<td align="right">0.7</td>
<td align="right">0.63</td>
<td align="right">0.33</td>
</tr>
<tr class="aad">
<td class="aad" height="17"><strong>Totals</strong></td>
<td align="right"><strong>2096</strong></td>
<td align="right"><strong>165.01</strong></td>
<td align="right"><strong>13.55</strong></td>
<td align="right"><strong>1.3</strong></td>
<td align="right"><strong>12.25</strong></td>
<td align="right"><strong>23.8</strong></td>
</tr>
<tr class="aad">
<td class="aad" height="17"><strong>Per Serving(/12)</strong></td>
<td align="right"><strong>174.67</strong></td>
<td align="right"><strong>13.75</strong></td>
<td align="right"><strong>1.13</strong></td>
<td align="right"><strong>0.11</strong></td>
<td align="right"><strong>1.02</strong></td>
<td align="right"><strong>1.98</strong></td>
</tr>
</tbody>
</table>
</html>"""), {
                'title':
                'Keto Beef Wellington',
                'url':
                'https://www.ruled.me/keto-beef-wellington/',
                'category':
                'entree',
                'ingredients': [
                    'sugar-free dark chocolate', 'coconut oil',
                    'heavy whipping cream', 'lemon zest', 'shredded coconut'
                ],
                'mainImage':
                None,
            })
