import os
import unittest

from scraper.common import errors
from scraper import html_parse


def _read_test_file(filename):
    basepath = os.path.dirname(__file__)
    filepath = os.path.join(basepath, 'testdata', filename)
    return open(filepath).read()


class HtmlParseTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_scrapes_ketoconnect_recipe(self):
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
                    u'Coconut flour',
                    u'psyilium husk powder',
                    u'active dry yeast',
                    u'Baking powder',
                    u'salt',
                    u'olive oil',
                    u'Water',
                    u'eggs',
                    u'minced garlic',
                    u'Red Pepper Flakes',
                    u'dried minced onion flakes',
                    u'Oregano',
                ],
                'mainImage':
                'https://ketoconnect-apjirmx5iktkd7.netdna-ssl.com/wp-content/uploads/2017/10/low-carb-pizza-crust-slice-flat.jpg',
                'publishedTime':
                '2017-10-08T09:52:09+00:00',
            })

    def test_scrapes_ruled_me_recipe(self):
        self.assertEqual(
            html_parse.
            parse({
                'url':
                'https://www.ruled.me/charred-veggie-fried-goat-cheese-salad/',
                'referer':
                'https://www.ruled.me/keto-recipes/lunch/page/3/',
            },
                  _read_test_file(
                      'ruled_me-charred-veggie-fried-goat-cheese-salad.html')),
            {
                'title':
                'Charred Veggie and Fried Goat Cheese Salad',
                'url':
                'https://www.ruled.me/charred-veggie-fried-goat-cheese-salad/',
                'category':
                'entree',
                'ingredients': [
                    u'poppy seeds',
                    u'sesame seeds',
                    u'onion flakes',
                    u'garlic flakes',
                    u'goat cheese',
                    u'medium red bell pepper',
                    u'sliced baby portobello mushrooms',
                    u'arugula',
                    u'avocado oil',
                ],
                'mainImage':
                'https://cdn4.ruled.me/wp-content/uploads/2017/09/fried-goat-cheese-salad-featured.jpg',
                'publishedTime':
                '2017-10-03T11:00:54+00:00',
            })

    def test_scrapes_ketogasm_recipe(self):
        self.assertEqual(
            html_parse.
            parse({
                'url':
                'https://ketogasm.com/smoked-pork-spare-ribs-chili-garlic-recipe/',
                'referer':
                'https://ketogasm.com/recipe-index/?fwp_recipes_filters=recipe',
            },
                  _read_test_file(
                      'ketogasm-com_smoked-pork-spare-ribs-chili-garlic-recipe.html'
                  )),
            {
                'title':
                'Smoked Pork Spare Ribs and Chili Garlic Sauce',
                'url':
                'https://ketogasm.com/smoked-pork-spare-ribs-chili-garlic-recipe/',
                'category':
                'entree',
                'ingredients': [
                    'pork spare ribs',
                    'Hickory wood chips/pellets',
                    'paprika',
                    'salt',
                    'pepper',
                    'onion powder',
                    'chili powder',
                    'ground mustard seed',
                    'coconut aminos',
                    'chili garlic sauce',
                    'yellow mustard',
                ],
                'mainImage':
                'https://ketogasm.com/wp-content/uploads/2017/10/2-smoked-pork-spare-ribs-chili-garlic-sauce.jpg',
                'publishedTime':
                '2017-10-30T12:00:22+00:00',
            })

    def test_fails_on_ketogasm_video_recipes(self):
        with self.assertRaises(errors.NoRecipeFoundError):
            html_parse.parse({
                'url':
                'https://ketogasm.com/how-to-make-loaded-fauxtato-skins-video/',
                'referer':
                'https://ketogasm.com/recipe-index/?fwp_recipes_filters=recipe',
            },
                             _read_test_file(
                                 'ketogasm-com_how-to-make-loaded-fauxtato-skins-video.html'
                             ))
