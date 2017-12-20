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

    def test_scrapes_hey_keto_mama_recipe(self):
        self.assertEqual(
            html_parse.parse({
                'url':
                'https://www.heyketomama.com/keto-white-chicken-chili/',
                'referer':
                'https://www.heyketomama.com/category/recipes/',
            }, _read_test_file(
                'heyketomama-com_keto-white-chicken-chili.html')),
            {
                'title':
                'Keto White Chicken Chili',
                'url':
                'https://www.heyketomama.com/keto-white-chicken-chili/',
                'category':
                None,
                'ingredients': [
                    u'chicken',
                    u'chicken broth',
                    u'garlic cloves, finely minced',
                    u'chopped green chiles',
                    u'diced jalapeno',
                    u'diced green pepper',
                    u'diced onion',
                    u'butter',
                    u'heavy whipping cream',
                    u'cream cheese',
                    u'cumin',
                    u'oregano',
                    u'cayenne',
                    u'Salt and Pepper',
                ],
                'mainImage':
                'https://www.heyketomama.com/wp-content/uploads/2017/10/keto-white-chicken-chili-sm.png',
                'publishedTime':
                '2017-10-30T01:02:11+00:00',
            })

    def test_scrapes_ketoconnect_recipe(self):
        self.assertEqual(
            html_parse.parse({
                'url':
                'https://www.ketoconnect.net/recipe/low-carb-pizza-crust/',
                'referer':
                'https://www.ketoconnect.net/main-dishes/',
            }, _read_test_file('low-carb-pizza-crust.html')), {
                'title':
                u'Low Carb Pizza Crust',
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
                u'https://ketoconnect-apjirmx5iktkd7.netdna-ssl.com/wp-content/uploads/2017/10/low-carb-pizza-crust-slice-flat.jpg',
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

    def test_scrapes_keto_size_me_recipe(self):
        self.assertEqual(
            html_parse.parse({
                'url':
                'https://ketosizeme.com/keto-baked-spaghetti/',
                'referer':
                'https://ketosizeme.com/ketogenic-diet-recipes-index/',
            }, _read_test_file('ketosizeme-com_keto-baked-spaghetti.html')), {
                'title':
                u'Keto Baked Spaghetti',
                'url':
                'https://ketosizeme.com/keto-baked-spaghetti/',
                'category':
                'entree',
                'ingredients': [
                    u'Ground Beef', u'Spaghetti Squash',
                    u'Wild Oats Organic Tomato Basil Pasta Sauce',
                    u'Frigo Shredded Parmesan Cheese',
                    u'Low Moisture Part-skim Mozzarella Cheese',
                    u'Wild Oats Organic Chili powder', u'Oregano',
                    u'Garlic Cloves', u'Large Egg'
                ],
                'mainImage':
                u'https://ketosizeme.com/wp-content/uploads/2015/05/Low-Carb-Keto-Baked-Spaghetti-.jpg',
                'publishedTime':
                '2015-10-20T03:09:44+00:00',
            })

    def test_scrapes_ketovangelist_kitchen_recipe(self):
        self.assertEqual(
            html_parse.
            parse({
                'url':
                'http://www.ketovangelistkitchen.com/lemon-shortbread-cookies/',
                'referer':
                'http://www.ketovangelistkitchen.com/category/baked-goods/',
            },
                  _read_test_file(
                      'ketovangelistkitchen-com_lemon-shortbread-cookies.html')
                 ),
            {
                'title':
                u'Lemon Shortbread Cookies',
                'url':
                'http://www.ketovangelistkitchen.com/lemon-shortbread-cookies/',
                'category':
                'dessert',
                'ingredients': [
                    u'almond flour',
                    u'chia seeds, finely ground',
                    u'xylitol',
                    u'xanthan gum',
                    u'Zest of lemons',
                    u'cold butter',
                ],
                'mainImage':
                'http://www.ketovangelistkitchen.com/wp-content/uploads/2016/12/2013-5-27-Lemon-Shortbread-Cookies-7567.jpg',
                'publishedTime':
                '2016-12-19T20:29:38+00:00',
            })

    def test_scrapes_ketovangelist_kitchen_recipe_unexpected_ingredients(self):
        self.assertEqual(
            html_parse.parse(
                {
                    'url':
                    'http://www.ketovangelistkitchen.com/creamy-cucumber-soup/',
                    'referer':
                    'http://www.ketovangelistkitchen.com/category/soup/',
                },
                _read_test_file(
                    'ketovangelistkitchen-com_creamy-cucumber-soup.html')),
            {
                'title':
                u'Creamy Cucumber Soup',
                'url':
                'http://www.ketovangelistkitchen.com/creamy-cucumber-soup/',
                'category':
                'side',
                'ingredients': [
                    u'coconut oil or avocado oil',
                    u'onion, chopped',
                    u'English cucumbers, chopped',
                    u'unsweetened thin coconut milk',
                    u'sea salt',
                    u'chopped fresh chives',
                    u'small avocados, skin and pits removed',
                    u'heavy cream',
                    u'white wine',
                    u'Chopped green onions for garnish',
                ],
                'mainImage':
                u'http://www.ketovangelistkitchen.com/wp-content/uploads/2017/01/2012-10-19-Creamy-Cucumber-Soup-4907.jpg',
                'publishedTime':
                '2017-01-23T08:15:03+00:00',
            })

    def test_scrapes_queen_bs_recipe(self):
        self.assertEqual(
            html_parse.
            parse({
                'url':
                'http://queenbsincredibleedibles.com/2017/09/19/dill-pickle-dip/',
                'referer':
                'http://queenbsincredibleedibles.com/category/keto/page/2/',
            },
                  _read_test_file(
                      'queenbsincredibleedibles-com_2017_09_19_dill-pickle-dip.html'
                  )),
            {
                'title':
                u'Dill Pickle Dip',
                'url':
                'http://queenbsincredibleedibles.com/2017/09/19/dill-pickle-dip/',
                'category':
                None,
                'ingredients': [
                    u'softened cream cheese',
                    u'dill pickle juice',
                    u'finely chopped pickle',
                    u'shredded Colby jack cheese',
                    u'crisped bacon',
                    u'thinly sliced scallions, plus more for garnish',
                ],
                'mainImage':
                u'http://queenbsincredibleedibles.com/wp-content/uploads/2017/09/img_6266.jpg',
                'publishedTime':
                '2017-09-19T10:00:46+00:00',
            })

    def test_scrapes_queen_bs_recipe_with_link_in_ingredients(self):
        self.assertEqual(
            html_parse.
            parse({
                'url':
                'http://queenbsincredibleedibles.com/2017/11/03/best-low-carb-gluten-free-stuffing-ever/',
                'referer':
                'http://queenbsincredibleedibles.com/category/keto/',
            },
                  _read_test_file(
                      'queenbsincredibleedibles-com_2017_11_03_best-low-carb-gluten-free-stuffing-ever.html'
                  )),
            {
                'title':
                u'The Best Low Carb Gluten-Free Stuffing Ever!',
                'url':
                'http://queenbsincredibleedibles.com/2017/11/03/best-low-carb-gluten-free-stuffing-ever/',
                'category':
                None,
                'ingredients': [
                    u'bread',
                    u'chicken stock or turkey stock',
                    u'fresh rosemary',
                    u'poultry seasoning',
                    u'garlic powder',
                    u'medium onion',
                    u'celery',
                    u'butter or olive oil',
                    u'Salt and pepper',
                ],
                'mainImage':
                u'http://queenbsincredibleedibles.com/wp-content/uploads/2017/11/img_7054.jpg',
                'publishedTime':
                '2017-11-03T10:00:53+00:00',
            })
