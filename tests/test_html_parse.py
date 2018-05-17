import os
import unittest

import mock

from scraper.common import errors
from scraper import html_parse


def _read_test_file(filename):
    basepath = os.path.dirname(__file__)
    filepath = os.path.join(basepath, 'testdata', filename)
    return open(filepath).read()


class HtmlParseUnitTest(unittest.TestCase):

    def setUp(self):
        self.mock_scraper = mock.Mock()
        self.mock_get_scraper_fn = mock.Mock()
        self.mock_get_scraper_fn.return_value = self.mock_scraper

        self.mock_ingredient_parser = mock.Mock()
        parser_patch = mock.patch.object(
            html_parse.ingredients.IngredientParser, 'parse',
            self.mock_ingredient_parser)
        self.addCleanup(parser_patch.stop)
        parser_patch.start()

    def test_retrieves_all_properties_from_scraper(self):
        self.mock_scraper.scrape_title.return_value = 'Dummy Hot Dogs'
        self.mock_scraper.scrape_category.return_value = 'Dinner'
        self.mock_scraper.scrape_ingredients.return_value = [u'salt', u'water']
        self.mock_scraper.scrape_image.return_value = 'http://a.b.com/img.jpg'
        self.mock_scraper.scrape_published_time.return_value = (
            '2018-05-05T12:28:35+00:00')

        self.mock_ingredient_parser.side_effect = [{
            u'comment': None,
            u'name': u'salt',
            u'other': None,
            u'quantity': None,
            u'unit': None
        }, {
            u'comment': None,
            u'name': u'water',
            u'other': None,
            u'quantity': None,
            u'unit': None
        }]

        self.assertEqual(
            html_parse.parse(
                metadata={
                    'url': 'http://ignored.url',
                },
                html='dummy file contents',
                parser_url='http://mock.ingredient.parser',
                get_scraper_fn=self.mock_get_scraper_fn), {
                    'title': 'Dummy Hot Dogs',
                    'url': 'http://ignored.url',
                    'category': 'Dinner',
                    'ingredients': [u'salt', u'water'],
                    'mainImage': 'http://a.b.com/img.jpg',
                    'publishedTime': '2018-05-05T12:28:35+00:00',
                })

    def test_absorbs_exception_on_category(self):
        self.mock_scraper.scrape_category.side_effect = ValueError(
            'dummy category scrape exception')

        self.mock_scraper.scrape_title.return_value = 'Dummy Hot Dogs'
        self.mock_scraper.scrape_ingredients.return_value = ['salt', 'water']
        self.mock_scraper.scrape_image.return_value = 'http://a.b.com/img.jpg'
        self.mock_scraper.scrape_published_time.return_value = (
            '2018-05-05T12:28:35+00:00')

        self.mock_ingredient_parser.side_effect = [{
            u'comment': None,
            u'name': u'salt',
            u'other': None,
            u'quantity': None,
            u'unit': None
        }, {
            u'comment': None,
            u'name': u'water',
            u'other': None,
            u'quantity': None,
            u'unit': None
        }]

        self.assertEqual(
            html_parse.parse(
                metadata={
                    'url': 'http://ignored.url',
                },
                html='dummy file contents',
                parser_url='http://mock.ingredient.parser',
                get_scraper_fn=self.mock_get_scraper_fn), {
                    'title': 'Dummy Hot Dogs',
                    'url': 'http://ignored.url',
                    'category': None,
                    'ingredients': [u'salt', u'water'],
                    'mainImage': 'http://a.b.com/img.jpg',
                    'publishedTime': '2018-05-05T12:28:35+00:00',
                })

    def test_absorbs_exception_on_ingredients(self):
        self.mock_scraper.scrape_ingredients.side_effect = ValueError(
            'dummy ingredients scrape exception')

        self.mock_scraper.scrape_title.return_value = 'Dummy Hot Dogs'
        self.mock_scraper.scrape_category.return_value = 'Dinner'
        self.mock_scraper.scrape_image.return_value = 'http://a.b.com/img.jpg'
        self.mock_scraper.scrape_published_time.return_value = (
            '2018-05-05T12:28:35+00:00')
        self.assertEqual(
            html_parse.parse(
                metadata={
                    'url': 'http://ignored.url',
                },
                html='dummy file contents',
                parser_url='http://mock.ingredient.parser',
                get_scraper_fn=self.mock_get_scraper_fn), {
                    'title': 'Dummy Hot Dogs',
                    'url': 'http://ignored.url',
                    'category': 'Dinner',
                    'ingredients': [],
                    'mainImage': 'http://a.b.com/img.jpg',
                    'publishedTime': '2018-05-05T12:28:35+00:00',
                })

    def test_absorbs_exception_on_published_time(self):
        self.mock_scraper.scrape_published_time.side_effect = ValueError(
            'dummy publish time scrape exception')

        self.mock_scraper.scrape_title.return_value = 'Dummy Hot Dogs'
        self.mock_scraper.scrape_category.return_value = 'Dinner'
        self.mock_scraper.scrape_ingredients.return_value = [u'salt', u'water']
        self.mock_scraper.scrape_image.return_value = 'http://a.b.com/img.jpg'

        self.mock_ingredient_parser.side_effect = [{
            u'comment': None,
            u'name': u'salt',
            u'other': None,
            u'quantity': None,
            u'unit': None
        }, {
            u'comment': None,
            u'name': u'water',
            u'other': None,
            u'quantity': None,
            u'unit': None
        }]

        self.assertEqual(
            html_parse.parse(
                metadata={
                    'url': 'http://ignored.url',
                },
                html='dummy file contents',
                parser_url='http://mock.ingredient.parser',
                get_scraper_fn=self.mock_get_scraper_fn), {
                    'title': 'Dummy Hot Dogs',
                    'url': 'http://ignored.url',
                    'category': 'Dinner',
                    'ingredients': [u'salt', u'water'],
                    'mainImage': 'http://a.b.com/img.jpg',
                    'publishedTime': None,
                })

    def test_passes_through_exception_on_title(self):
        self.mock_scraper.scrape_title.side_effect = ValueError(
            'dummy title scrape exception')

        self.mock_scraper.scrape_category.return_value = 'Dinner'
        self.mock_scraper.scrape_ingredients.return_value = [u'salt', u'water']
        self.mock_scraper.scrape_image.return_value = 'http://a.b.com/img.jpg'
        self.mock_scraper.scrape_published_time.return_value = (
            '2018-05-05T12:28:35+00:00')
        with self.assertRaises(ValueError):
            html_parse.parse(
                metadata={
                    'url': 'http://ignored.url',
                },
                html='dummy file contents',
                parser_url='http://mock.ingredient.parser',
                get_scraper_fn=self.mock_get_scraper_fn)

    def test_raises_NoRecipeFoundError_if_title_is_missing(self):
        self.mock_scraper.scrape_title.return_value = None

        self.mock_scraper.scrape_category.return_value = 'Dinner'
        self.mock_scraper.scrape_ingredients.return_value = [u'salt', u'water']
        self.mock_scraper.scrape_image.return_value = 'http://a.b.com/img.jpg'
        self.mock_scraper.scrape_published_time.return_value = (
            '2018-05-05T12:28:35+00:00')
        with self.assertRaises(errors.NoRecipeFoundError):
            html_parse.parse(
                metadata={
                    'url': 'http://ignored.url',
                },
                html='dummy file contents',
                parser_url='http://mock.ingredient.parser',
                get_scraper_fn=self.mock_get_scraper_fn)

    def test_raises_NoRecipeFoundError_if_title_is_empty(self):
        self.mock_scraper.scrape_title.return_value = ''

        self.mock_scraper.scrape_category.return_value = 'Dinner'
        self.mock_scraper.scrape_ingredients.return_value = [u'salt', u'water']
        self.mock_scraper.scrape_image.return_value = 'http://a.b.com/img.jpg'
        self.mock_scraper.scrape_published_time.return_value = (
            '2018-05-05T12:28:35+00:00')
        with self.assertRaises(errors.NoRecipeFoundError):
            html_parse.parse(
                metadata={
                    'url': 'http://ignored.url',
                },
                html='dummy file contents',
                parser_url='http://mock.ingredient.parser',
                get_scraper_fn=self.mock_get_scraper_fn)

    def test_passes_through_exception_on_image(self):
        self.mock_scraper.scrape_image.side_effect = ValueError(
            'dummy image scrape exception')

        self.mock_scraper.scrape_title.return_value = 'Dummy Hot Dogs'
        self.mock_scraper.scrape_category.return_value = 'Dinner'
        self.mock_scraper.scrape_ingredients.return_value = [u'salt', u'water']
        self.mock_scraper.scrape_published_time.return_value = (
            '2018-05-05T12:28:35+00:00')

        with self.assertRaises(ValueError):
            html_parse.parse(
                metadata={
                    'url': 'http://ignored.url',
                },
                html='dummy file contents',
                parser_url='http://mock.ingredient.parser',
                get_scraper_fn=self.mock_get_scraper_fn)

    def test_raises_NoRecipeFoundError_if_main_image_is_missing(self):
        self.mock_scraper.scrape_image.return_value = None

        self.mock_scraper.scrape_title.return_value = 'Dummy Hot Dogs'
        self.mock_scraper.scrape_category.return_value = 'Dinner'
        self.mock_scraper.scrape_ingredients.return_value = [u'salt', u'water']
        self.mock_scraper.scrape_published_time.return_value = (
            '2018-05-05T12:28:35+00:00')
        with self.assertRaises(errors.NoRecipeFoundError):
            html_parse.parse(
                metadata={
                    'url': 'http://ignored.url',
                },
                html='dummy file contents',
                parser_url='http://mock.ingredient.parser',
                get_scraper_fn=self.mock_get_scraper_fn)

    def test_raises_NoRecipeFoundError_if_main_image_is_empty(self):
        self.mock_scraper.scrape_image.return_value = ''

        self.mock_scraper.scrape_title.return_value = 'Dummy Hot Dogs'
        self.mock_scraper.scrape_category.return_value = 'Dinner'
        self.mock_scraper.scrape_ingredients.return_value = [u'salt', u'water']
        self.mock_scraper.scrape_published_time.return_value = (
            '2018-05-05T12:28:35+00:00')
        with self.assertRaises(errors.NoRecipeFoundError):
            html_parse.parse(
                metadata={
                    'url': 'http://ignored.url',
                },
                html='dummy file contents',
                parser_url='http://mock.ingredient.parser',
                get_scraper_fn=self.mock_get_scraper_fn)


class HtmlParseTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

        self.mock_ingredient_parser = mock.Mock()
        parser_patch = mock.patch.object(
            html_parse.ingredients.IngredientParser, 'parse',
            self.mock_ingredient_parser)
        self.addCleanup(parser_patch.stop)
        parser_patch.start()

    def test_scrapes_hey_keto_mama_recipe(self):
        parsed_ingredients = [{
            u'comment': None,
            u'other': u'lb',
            u'name': u'chicken',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': u'1.5',
            u'name': u'chicken broth',
            u'unit': u'cup',
            u'quantity': 1.0
        }, {
            u'comment': u'finely minced',
            u'other': u',',
            u'name': u'garlic',
            u'unit': u'clove',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'4.5 ounces can chopped green chiles',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': u'diced',
            u'other': None,
            u'name': u'jalapeno',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': u'diced',
            u'other': None,
            u'name': u'green pepper',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': u'diced',
            u'other': None,
            u'name': u'onion',
            u'unit': u'cup',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tbsp butter',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'heavy whipping cream',
            u'unit': u'cup',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': u'oz',
            u'name': u'cream cheese',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tsp cumin',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tsp oregano',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': u'1\\/4 tsp',
            u'name': u'cayenne',
            u'unit': None,
            u'quantity': 1.0
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'Salt and Pepper to taste',
            u'unit': None,
            u'quantity': None
        }]
        self.mock_ingredient_parser.side_effect = parsed_ingredients

        self.assertEqual(
            html_parse.parse(
                {
                    'url':
                    'https://www.heyketomama.com/keto-white-chicken-chili/',
                    'referer': 'https://www.heyketomama.com/category/recipes/',
                },
                _read_test_file(
                    'heyketomama-com_keto-white-chicken-chili.html'),
                'http://mock.ingredient.parser'),
            {
                'title':
                'Keto White Chicken Chili',
                'url':
                'https://www.heyketomama.com/keto-white-chicken-chili/',
                'category':
                None,
                'ingredients': [
                    u'chicken', u'chicken broth', u'garlic',
                    u'4.5 ounces can chopped green chiles', u'jalapeno',
                    u'green pepper', u'onion', u'tbsp butter',
                    u'heavy whipping cream', u'cream cheese', u'tsp cumin',
                    u'tsp oregano', u'cayenne', u'Salt and Pepper to taste'
                ],
                'mainImage':
                'https://www.heyketomama.com/wp-content/uploads/2017/10/keto-white-chicken-chili-sm.png',
                'publishedTime':
                '2017-10-30T01:02:11+00:00',
            })

        self.assertEqual(
            [call[0][0]
             for call in self.mock_ingredient_parser.call_args_list], [
                 u'1 lb chicken', u'1.5 cups chicken broth',
                 u'2 garlic cloves, finely minced',
                 u'1 4.5oz can chopped green chiles', u'1 diced jalapeno',
                 u'1 diced green pepper', u'1/4 cup diced onion',
                 u'4 tbsp butter', u'1/4 cup heavy whipping cream',
                 u'4 oz cream cheese', u'2 tsp cumin', u'1 tsp oregano',
                 u'1/4 tsp cayenne (optional)', u'Salt and Pepper to taste'
             ])

    def test_scrapes_ketoconnect_recipe(self):
        parsed_ingredients = [{
            u'comment': None,
            u'other': None,
            u'name': u'Coconut flour',
            u'unit': u'cup',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'psyilium husk powder',
            u'unit': u'cup',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tsp active dry yeast',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'1\\/2 tsp Baking powder',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': u'1\\/4 tsp',
            u'name': u'salt',
            u'unit': None,
            u'quantity': 1.0
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'olive oil',
            u'unit': u'cup',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'Water',
            u'unit': u'cup',
            u'quantity': None
        }, {
            u'comment': u'large',
            u'other': None,
            u'name': u'eggs',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': u'tsp minced',
            u'name': u'garlic',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'1\\/2 tsp Red Pepper Flakes',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'1\\/2 tsp dried minced onion flakes',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'1\\/2 tsp Oregano',
            u'unit': None,
            u'quantity': None
        }]

        self.mock_ingredient_parser.side_effect = parsed_ingredients
        self.assertEqual(
            html_parse.parse({
                'url':
                'https://www.ketoconnect.net/recipe/low-carb-pizza-crust/',
                'referer':
                'https://www.ketoconnect.net/main-dishes/',
            },
                             _read_test_file('low-carb-pizza-crust.html'),
                             'http://mock.ingredient.parser'),
            {
                'title':
                u'Low Carb Pizza Crust',
                'url':
                'https://www.ketoconnect.net/recipe/low-carb-pizza-crust/',
                'category':
                'entree',
                'ingredients': [
                    u'Coconut flour', u'psyilium husk powder',
                    u'tsp active dry yeast', u'1\\/2 tsp Baking powder',
                    u'salt', u'olive oil', u'Water', u'eggs', u'garlic',
                    u'1\\/2 tsp Red Pepper Flakes',
                    u'1\\/2 tsp dried minced onion flakes', u'1\\/2 tsp Oregano'
                ],
                'mainImage':
                u'https://ketoconnect-apjirmx5iktkd7.netdna-ssl.com/wp-content/uploads/2017/10/low-carb-pizza-crust-slice-flat.jpg',
                'publishedTime':
                '2017-10-08T09:52:09+00:00',
            })
        self.assertEqual(
            [call[0][0]
             for call in self.mock_ingredient_parser.call_args_list], [
                 u'Coconut flour', u'psyilium husk powder', u'active dry yeast',
                 u'Baking powder', u'salt', u'olive oil', u'Water', u'eggs',
                 u'minced garlic', u'Red Pepper Flakes',
                 u'dried minced onion flakes', u'Oregano'
             ])

    def test_scrapes_ruled_me_recipe(self):
        parsed_ingredients = [{
            u'comment': None,
            u'other': None,
            u'name': u'poppy seeds',
            u'unit': u'tablespoon',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'sesame seeds',
            u'unit': u'tablespoon',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'onion flakes',
            u'unit': u'teaspoon',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'garlic flakes',
            u'unit': u'teaspoon',
            u'quantity': None
        }, {
            u'comment':
            u'cut into 4 \xbd in thick medallions',
            u'other':
            u',',
            u'name':
            u'goat cheese',
            u'unit':
            u'ounce',
            u'quantity':
            None
        }, {
            u'comment':
            u'medium, seeds removed, cut into 8 pieces',
            u'other':
            None,
            u'name':
            u'red bell pepper',
            u'unit':
            None,
            u'quantity':
            None
        }, {
            u'comment': u'sliced',
            u'other': None,
            u'name': u'baby portobello mushrooms',
            u'unit': u'cup',
            u'quantity': None
        }, {
            u'comment': u'divided between two bowls',
            u'other': u',',
            u'name': u'arugula',
            u'unit': u'cup',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'avocado oil',
            u'unit': u'tablespoon',
            u'quantity': None
        }]

        self.mock_ingredient_parser.side_effect = parsed_ingredients
        self.assertEqual(
            html_parse.
            parse({
                'url':
                'https://www.ruled.me/charred-veggie-fried-goat-cheese-salad/',
                'referer':
                'https://www.ruled.me/keto-recipes/lunch/page/3/',
            },
                  _read_test_file(
                      'ruled_me-charred-veggie-fried-goat-cheese-salad.html'),
                  'http://mock.ingredient.parser'),
            {
                'title':
                'Charred Veggie and Fried Goat Cheese Salad',
                'url':
                'https://www.ruled.me/charred-veggie-fried-goat-cheese-salad/',
                'category':
                'entree',
                'ingredients': [
                    u'poppy seeds', u'sesame seeds', u'onion flakes',
                    u'garlic flakes', u'goat cheese', u'red bell pepper',
                    u'baby portobello mushrooms', u'arugula', u'avocado oil'
                ],
                'mainImage':
                'https://cdn4.ruled.me/wp-content/uploads/2017/09/fried-goat-cheese-salad-featured.jpg',
                'publishedTime':
                '2017-10-03T11:00:54+00:00',
            })
        self.assertEqual(
            [call[0][0]
             for call in self.mock_ingredient_parser.call_args_list], [
                 u'2 tablespoons poppy seeds', u'2 tablespoons sesame seeds',
                 u'1 teaspoon onion flakes', u'1 teaspoon garlic flakes',
                 u'4 ounces goat cheese', u'1 medium (119 g) red bell pepper',
                 u'\xbd cup sliced baby portobello mushrooms',
                 u'4 cups (80 g) arugula', u'1 tablespoon avocado oil'
             ])

    def test_scrapes_ketogasm_recipe(self):
        parsed_ingredients = [{
            u'comment': None,
            u'other': None,
            u'name': u'pork spare ribs',
            u'unit': u'pound',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'Hickory wood chips\\/pellets',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'paprika',
            u'unit': u'tbsp',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tbsp salt',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tbsp pepper',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tsp onion powder',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tsp chili powder',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'1\\/2 tsp ground mustard seed',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'coconut aminos',
            u'unit': u'cup',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tbsp chili garlic sauce',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tbsp yellow mustard',
            u'unit': None,
            u'quantity': None
        }]
        self.mock_ingredient_parser.side_effect = parsed_ingredients
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
                  ), 'http://mock.ingredient.parser'),
            {
                'title':
                'Smoked Pork Spare Ribs and Chili Garlic Sauce',
                'url':
                'https://ketogasm.com/smoked-pork-spare-ribs-chili-garlic-recipe/',
                'category':
                'entree',
                'ingredients': [
                    u'pork spare ribs', u'Hickory wood chips\\/pellets',
                    u'paprika', u'tbsp salt', u'tbsp pepper',
                    u'tsp onion powder', u'tsp chili powder',
                    u'1\\/2 tsp ground mustard seed', u'coconut aminos',
                    u'tbsp chili garlic sauce', u'tbsp yellow mustard'
                ],
                'mainImage':
                'https://ketogasm.com/wp-content/uploads/2017/10/2-smoked-pork-spare-ribs-chili-garlic-sauce.jpg',
                'publishedTime':
                '2017-10-30T12:00:22+00:00',
            })

        self.assertEqual(
            [call[0][0]
             for call in self.mock_ingredient_parser.call_args_list], [
                 u'6 pounds pork spare ribs', u'Hickory wood chips/pellets',
                 u'2 tbsp paprika', u'2 tbsp salt', u'2 tbsp pepper',
                 u'1 tsp onion powder', u'1 tsp chili powder',
                 u'1/2 tsp ground mustard seed', u'1/4 cup coconut aminos',
                 u'2 tbsp chili garlic sauce', u'1 tbsp yellow mustard'
             ])

    def test_scrapes_ketogasm_recipe_with_html_encoded_ingredients(self):
        parsed_ingredients = [{
            u'comment': None,
            u'other': u'oz',
            u'name': u'spinach',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tsp ghee',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': u'oz',
            u'name': u'mushrooms',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': u'14 oz smoked',
            u'name': u'sausage',
            u'unit': None,
            u'quantity': 14.0
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'garlic',
            u'unit': u'clove',
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'salt &amp; pepper',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'eggs',
            u'unit': None,
            u'quantity': None
        }]
        self.mock_ingredient_parser.side_effect = parsed_ingredients
        self.assertEqual(
            html_parse.
            parse({
                'url':
                'https://ketogasm.com/smoked-sausage-frittata-recipe-with-spinach-mushroom/',
                'referer':
                'https://ketogasm.com/recipe-index/?fwp_recipes_filters=recipe',
            },
                  _read_test_file(
                      'ketogasm-com_smoked-sausage-frittata-recipe-with-spinach-mushroom.html'
                  ), 'http://mock.ingredient.parser'),
            {
                'title':
                u'Smoked Sausage Frittata with Spinach and Mushroom',
                'url':
                'https://ketogasm.com/smoked-sausage-frittata-recipe-with-spinach-mushroom/',
                'category':
                'breakfast',
                'ingredients': [
                    u'spinach', u'tsp ghee', u'mushrooms', u'sausage',
                    u'garlic', u'salt &amp; pepper', u'eggs'
                ],
                'mainImage':
                u'https://cdn1.ketogasm.com/wp-content/uploads/2017/11/1-smoked-sausage-frittata-recipe-spinach-mushroom-low-carb-keto-dairy-free.jpg',
                'publishedTime':
                '2017-11-17T12:00:07+00:00',
            })
        self.assertEqual([
            call[0][0] for call in self.mock_ingredient_parser.call_args_list
        ], [
            u'10 oz spinach (raw)', u'1 tsp ghee', u'4 oz mushrooms (sliced)',
            u'14 oz smoked sausage (uncured, chopped)',
            u'1 clove garlic (minced)', u'salt & pepper  (to taste)', u'8  eggs'
        ])

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
                             ), 'http://mock.ingredient.parser')

    def test_scrapes_keto_size_me_recipe(self):
        parsed_ingredients = [{
            u'comment': u'Ground',
            u'other': u'lb',
            u'name': u'Beef',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'Spaghetti Squash',
            u'unit': u'cup',
            u'quantity': None
        }, {
            u'comment':
            None,
            u'other':
            None,
            u'name':
            u'container Wild Oats Organic Tomato Basil Pasta Sauce',
            u'unit':
            None,
            u'quantity':
            None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'Frigo Shredded Parmesan Cheese',
            u'unit': u'cup',
            u'quantity': None
        }, {
            u'comment':
            None,
            u'other':
            None,
            u'name':
            u'Low Moisture Part-skim Mozzarella Cheese',
            u'unit':
            u'cup',
            u'quantity':
            None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tsp Wild Oats Organic Chili powder',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'tsp Oregano',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'Garlic Cloves',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': None,
            u'name': u'Large Egg',
            u'unit': None,
            u'quantity': None
        }]
        self.mock_ingredient_parser.side_effect = parsed_ingredients
        self.assertEqual(
            html_parse.parse(
                {
                    'url':
                    'https://ketosizeme.com/keto-baked-spaghetti/',
                    'referer':
                    'https://ketosizeme.com/ketogenic-diet-recipes-index/',
                },
                _read_test_file('ketosizeme-com_keto-baked-spaghetti.html'),
                'http://mock.ingredient.parser'),
            {
                'title':
                u'Keto Baked Spaghetti',
                'url':
                'https://ketosizeme.com/keto-baked-spaghetti/',
                'category':
                'entree',
                'ingredients': [
                    u'Beef', u'Spaghetti Squash',
                    u'container Wild Oats Organic Tomato Basil Pasta Sauce',
                    u'Frigo Shredded Parmesan Cheese',
                    u'Low Moisture Part-skim Mozzarella Cheese',
                    u'tsp Wild Oats Organic Chili powder', u'tsp Oregano',
                    u'Garlic Cloves', u'Large Egg'
                ],
                'mainImage':
                u'https://ketosizeme.com/wp-content/uploads/2015/05/Low-Carb-Keto-Baked-Spaghetti-.jpg',
                'publishedTime':
                '2015-10-20T03:09:44+00:00',
            })
        self.assertEqual(
            [call[0][0]
             for call in self.mock_ingredient_parser.call_args_list], [
                 u'1 lb Ground Beef (cooked & drained)',
                 u'4 cups Spaghetti Squash (cooked)',
                 u'1 container Wild Oats Organic Tomato Basil Pasta Sauce',
                 u'1 1/2 cups Frigo Shredded Parmesan Cheese',
                 u'3 1/2 cups Low Moisture Part-skim Mozzarella Cheese',
                 u'1 tsp Wild Oats Organic Chili powder', u'1/2 tsp Oregano',
                 u'2 Garlic Cloves', u'1 Large Egg'
             ])

    def test_scrapes_ketovangelist_kitchen_recipe(self):
        parsed_ingredients = [{
            u'comment': None,
            u'other': u'oz. / 200 grams',
            u'name': u'almond flour',
            u'unit': None,
            u'quantity': 200.0
        }, {
            u'comment': None,
            u'other': u'oz. / 30 grams',
            u'name': u'chia seeds, \xa0finely ground',
            u'unit': None,
            u'quantity': 30.0
        }, {
            u'comment': None,
            u'other': u'2\xbd oz. / 70 grams',
            u'name': u'xylitol',
            u'unit': None,
            u'quantity': 2.0
        }, {
            u'comment': None,
            u'other': u'tsp.',
            u'name': u'xanthan gum',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': u'Zest of',
            u'other': None,
            u'name': u'lemons',
            u'unit': None,
            u'quantity': None
        }, {
            u'comment': None,
            u'other': u'oz. / 85 grams cold',
            u'name': u'butter',
            u'unit': None,
            u'quantity': 85.0
        }]
        self.mock_ingredient_parser.side_effect = parsed_ingredients
        self.assertEqual(
            html_parse.
            parse({
                'url':
                'http://www.ketovangelistkitchen.com/lemon-shortbread-cookies/',
                'referer':
                'http://www.ketovangelistkitchen.com/category/baked-goods/',
            },
                  _read_test_file(
                      'ketovangelistkitchen-com_lemon-shortbread-cookies.html'),
                  'http://mock.ingredient.parser'),
            {
                'title':
                u'Lemon Shortbread Cookies',
                'url':
                'http://www.ketovangelistkitchen.com/lemon-shortbread-cookies/',
                'category':
                'dessert',
                'ingredients': [
                    u'almond flour', u'chia seeds, \xa0finely ground',
                    u'xylitol', u'xanthan gum', u'lemons', u'butter'
                ],
                'mainImage':
                'http://www.ketovangelistkitchen.com/wp-content/uploads/2016/12/2013-5-27-Lemon-Shortbread-Cookies-7567.jpg',
                'publishedTime':
                '2016-12-19T20:29:38+00:00',
            })
        self.assertEqual(
            [call[0][0]
             for call in self.mock_ingredient_parser.call_args_list], [
                 u'7 oz. / 200g almond flour (blanched ground almonds)',
                 u'1 oz. / 30g chia seeds,\xa0finely ground',
                 u'2\xbd oz. / 70g xylitol', u'1 tsp. xanthan gum',
                 u'Zest of 2 lemons', u'3 oz. / 85g cold butter'
             ])

    def test_scrapes_ketovangelist_kitchen_recipe_unexpected_ingredients(self):
        parsed_ingredients = [
            {
                u'comment': u'or avocado',
                u'other': None,
                u'name': u'TBSP coconut oil oil',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': u', chopped',
                u'other': u'oz. / 140 grams',
                u'name': u'onion',
                u'unit': None,
                u'quantity': 140.0
            },
            {
                u'comment': None,
                u'other': u'\xbd lb / 1120 grams',
                u'name': u'English cucumbers, chopped',
                u'unit': None,
                u'quantity': 1120.0
            },
            {
                u'comment': u'unsweetened thin',
                u'other': u'\xbd / 12 fl oz.',
                u'name': u'coconut milk',
                u'unit': u'cup',
                u'quantity': 12.0
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'tsp sea salt',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'chopped fresh chives',
                u'unit': u'cup',
                u'quantity': None
            },
            {
                u'comment': u'small, skin and pits removed',
                u'other': None,
                u'name': u'avocados',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'TBSP heavy cream',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'TBSP white wine',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': u'Chopped green for garnish',
                u'other': None,
                u'name': u'onions',
                u'unit': None,
                u'quantity': None
            },
        ]
        self.mock_ingredient_parser.side_effect = parsed_ingredients
        self.assertEqual(
            html_parse.parse(
                {
                    'url':
                    'http://www.ketovangelistkitchen.com/creamy-cucumber-soup/',
                    'referer':
                    'http://www.ketovangelistkitchen.com/category/soup/',
                },
                _read_test_file(
                    'ketovangelistkitchen-com_creamy-cucumber-soup.html'),
                'http://mock.ingredient.parser'),
            {
                'title':
                u'Creamy Cucumber Soup',
                'url':
                'http://www.ketovangelistkitchen.com/creamy-cucumber-soup/',
                'category':
                'side',
                'ingredients': [
                    u'TBSP coconut oil oil', u'onion',
                    u'English cucumbers, chopped', u'coconut milk',
                    u'tsp sea salt', u'chopped fresh chives', u'avocados',
                    u'TBSP heavy cream', u'TBSP white wine', u'onions'
                ],
                'mainImage':
                u'http://www.ketovangelistkitchen.com/wp-content/uploads/2017/01/2012-10-19-Creamy-Cucumber-Soup-4907.jpg',
                'publishedTime':
                '2017-01-23T08:15:03+00:00',
            })
        self.assertEqual([
            call[0][0] for call in self.mock_ingredient_parser.call_args_list
        ], [
            u'2 TBSP coconut oil or avocado oil',
            u'5 oz. / 140g onion, chopped',
            u'2 \xbd lb / 1120g English cucumbers, chopped',
            u'1 \xbd cups / 12 fl oz. unsweetened thin coconut milk (in a carton)',
            u'3 tsp sea salt', u'\xbd cup chopped fresh chives',
            u'2 small avocados, skin and pits removed',
            u'2 TBSP heavy cream (double cream)', u'1 TBSP white wine',
            u'Chopped green onions (scallions) for garnish'
        ])

    def test_scrapes_low_carb_yum_recipe(self):
        parsed_ingredients = [
            {
                u'comment': None,
                u'other': u'on the half shell',
                u'name': u'sea scallops',
                u'unit': u'piece',
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'garlic',
                u'unit': u'clove',
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'butter',
                u'unit': u'tablespoon',
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': u'1/3',
                u'name': u'cheddar cheese',
                u'unit': u'cup',
                u'quantity': 1.0
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'mozzarella',
                u'unit': u'cup',
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': u'1/3',
                u'name': u'heavy cream',
                u'unit': u'cup',
                u'quantity': 1.0
            },
            {
                u'comment': None,
                u'other': u'1/3',
                u'name': u'pork rind',
                u'unit': u'cup',
                u'quantity': 1.0
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'jalape\xf1os',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'lemons',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'salt and black Pepper',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': u'for garnishing',
                u'other': u'fresh',
                u'name': u'parsley',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'hot water for soaking shells',
                u'unit': None,
                u'quantity': None
            },
        ]
        self.mock_ingredient_parser.side_effect = parsed_ingredients
        self.assertEqual(
            html_parse.parse(
                {
                    'url': 'https://lowcarbyum.com/baked-sea-scallops/',
                    'referer': 'https://lowcarbyum.com/recipes/',
                },
                _read_test_file('lowcarbyum-com_baked-sea-scallops.html'),
                'http://mock.ingredient.parser'),
            {
                'title':
                u'Baked Sea Scallops with Crispy Gluten-Free Topping',
                'url':
                'https://lowcarbyum.com/baked-sea-scallops/',
                'category':
                'appetizer',
                'ingredients': [
                    u'sea scallops', u'garlic', u'butter', u'cheddar cheese',
                    u'mozzarella', u'heavy cream', u'pork rind',
                    u'jalape\xf1os', u'lemons', u'salt and black Pepper',
                    u'parsley', u'hot water for soaking shells'
                ],
                'mainImage':
                u'https://lowcarbyum.com/wp-content/uploads/2017/08/baked-sea-scallops-l.jpg',
                'publishedTime':
                '2017-08-11T05:26:46+00:00',
            })

        self.assertEqual([
            call[0][0] for call in self.mock_ingredient_parser.call_args_list
        ], [
            u'10 pieces sea scallops on the half shell (375g each without shell)',
            u'4 cloves garlic (finely chopped)', u'2 tablespoons butter',
            u'1/3 cup cheddar cheese (Freshly Grated)', u'3/4 cup mozzarella',
            u'1/3 cup heavy cream', u'1/3 cup pork rind',
            u'2  jalape\xf1os (thinly sliced)', u'2  lemons (juice and slices)',
            u'salt and black Pepper (to taste)',
            u'fresh parsley for garnishing', u'hot water for soaking shells'
        ])

    def test_raises_error_on_low_carb_yum_non_recipe_post(self):
        with self.assertRaises(errors.NoRecipeFoundError):
            html_parse.parse(
                {
                    'url':
                    'https://lowcarbyum.com/bacon-wrapped-cheese-sticks/',
                    'referer': 'https://lowcarbyum.com/recipes/',
                },
                _read_test_file(
                    'lowcarbyum-com_bacon-wrapped-cheese-sticks.html'),
                'http://mock.ingredient.parser')

    def test_scrapes_low_carb_yum_recipe_with_trailing_title_tag(self):
        parsed_ingredients = [
            {
                u'comment': None,
                u'other': u'of',
                u'name': u'NatureRaised Farms\xae Bacon',
                u'unit': u'slice',
                u'quantity': None
            },
            {
                u'comment': u'large',
                u'other': None,
                u'name': u'eggs',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'cheddar cheese',
                u'unit': u'ounce',
                u'quantity': None
            },
        ]
        self.mock_ingredient_parser.side_effect = parsed_ingredients
        self.assertEqual(
            html_parse.
            parse({
                'url':
                'https://lowcarbyum.com/low-carb-egg-muffins-wrapped-bacon/',
                'referer':
                'https://lowcarbyum.com/recipes/',
            },
                  _read_test_file(
                      'lowcarbyum-com_low-carb-egg-muffins-wrapped-bacon.html'),
                  'http://mock.ingredient.parser'),
            {
                'title':
                u'Low Carb Egg Muffins Wrapped in Bacon',
                'url':
                'https://lowcarbyum.com/low-carb-egg-muffins-wrapped-bacon/',
                'category':
                'breakfast',
                'ingredients':
                [u'NatureRaised Farms\xae Bacon', u'eggs', u'cheddar cheese'],
                'mainImage':
                u'https://lowcarbyum.com/wp-content/uploads/2016/10/low-carb-egg-muffins-wrapped-bacon-sq.jpg',
                'publishedTime':
                '2016-11-19T10:26:25+00:00',
            })
        self.assertEqual(
            [call[0][0]
             for call in self.mock_ingredient_parser.call_args_list], [
                 u'12 slices of NatureRaised Farms\xae Bacon',
                 u'12  large eggs', u'8 ounces cheddar cheese (grated)'
             ])

    def test_scrapes_queen_bs_recipe(self):
        parsed_ingredients = [
            {
                u'comment': u'softened',
                u'other': None,
                u'name': u'cream cheese',
                u'unit': u'ounce',
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'dill pickle juice',
                u'unit': u'cup',
                u'quantity': None
            },
            {
                u'comment': u'finely chopped',
                u'other': None,
                u'name': u'pickle',
                u'unit': u'cup',
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': u', separated in 1/4 cups',
                u'name': u'shredded Colby jack cheese',
                u'unit': u'cup',
                u'quantity': 1.0
            },
            {
                u'comment': None,
                u'other': u'\u2013 chopped and separated in 1/4 cups',
                u'name': u'crisped bacon',
                u'unit': u'cup',
                u'quantity': 1.0
            },
            {
                u'comment': u'thinly sliced, plus more for garnish, if desired',
                u'other': None,
                u'name': u'scallions',
                u'unit': u'cup',
                u'quantity': None
            },
        ]
        self.mock_ingredient_parser.side_effect = parsed_ingredients
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
                  ), 'http://mock.ingredient.parser'),
            {
                'title':
                u'Dill Pickle Dip',
                'url':
                'http://queenbsincredibleedibles.com/2017/09/19/dill-pickle-dip/',
                'category':
                None,
                'ingredients': [
                    u'cream cheese', u'dill pickle juice', u'pickle',
                    u'shredded Colby jack cheese', u'crisped bacon',
                    u'scallions'
                ],
                'mainImage':
                u'http://queenbsincredibleedibles.com/wp-content/uploads/2017/09/img_6266.jpg',
                'publishedTime':
                '2017-09-19T10:00:46+00:00',
            })
        self.assertEqual([
            call[0][0] for call in self.mock_ingredient_parser.call_args_list
        ], [
            u'8 ounces softened cream cheese', u'1/4 cup dill pickle juice',
            u'1/4 cup finely chopped pickle',
            u'1/2 cup shredded Colby jack cheese, separated in 1/4 cups',
            u'1/2 cup crisped bacon \u2013 chopped and separated in 1/4 cups',
            u'1/4 cup thinly sliced scallions, plus more for garnish, if desired'
        ])

    def test_scrapes_queen_bs_recipe_with_link_in_ingredients(self):
        parsed_ingredients = [
            {
                u'comment': None,
                u'other': None,
                u'name': u'bread cubes',
                u'unit': u'cup',
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': u'1.5',
                u'name': u'chicken stock or turkey stock',
                u'unit': u'cup',
                u'quantity': 1.0
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'tsp fresh rosemary',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'tsp poultry seasoning',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'tbsp garlic powder',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': u'medium',
                u'other': None,
                u'name': u'onion',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'celery',
                u'unit': u'stalk',
                u'quantity': None
            },
            {
                u'comment': u'tbsp or olive',
                u'other': None,
                u'name': u'butter oil',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'Salt and pepper',
                u'unit': None,
                u'quantity': None
            },
        ]
        self.mock_ingredient_parser.side_effect = parsed_ingredients
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
                  ), 'http://mock.ingredient.parser'),
            {
                'title':
                u'The Best Low Carb Gluten-Free Stuffing Ever!',
                'url':
                'http://queenbsincredibleedibles.com/2017/11/03/best-low-carb-gluten-free-stuffing-ever/',
                'category':
                None,
                'ingredients': [
                    u'bread cubes', u'chicken stock or turkey stock',
                    u'tsp fresh rosemary', u'tsp poultry seasoning',
                    u'tbsp garlic powder', u'onion', u'celery', u'butter oil',
                    u'Salt and pepper'
                ],
                'mainImage':
                u'http://queenbsincredibleedibles.com/wp-content/uploads/2017/11/img_7054.jpg',
                'publishedTime':
                '2017-11-03T10:00:53+00:00',
            })
        self.assertEqual(
            [call[0][0]
             for call in self.mock_ingredient_parser.call_args_list], [
                 u'6 cups bread cubes (made with KetoFoccacia)',
                 u'1.5 cups chicken stock or turkey stock',
                 u'1 tsp fresh rosemary', u'1 tsp poultry seasoning',
                 u'1 tbsp garlic powder', u'1 medium onion', u'3 stalks celery',
                 u'3 tbsp butter or olive oil', u'Salt and pepper'
             ])

    def test_raises_exception_on_queen_bs_page_without_recipe(self):
        with self.assertRaises(errors.NoRecipeFoundError):
            html_parse.parse(
                {
                    'url':
                    'http://queenbsincredibleedibles.com/category/baking/',
                    'referer':
                    'http://queenbsincredibleedibles.com/category/keto/',
                },
                _read_test_file(
                    'queenbsincredibleedibles-com_category_baking.html'),
                'http://mock.ingredient.parser')

    def test_scrapes_your_friends_j_recipe(self):
        parsed_ingredients = [
            {
                u'comment': None,
                u'other': None,
                u'name': u'Roma Tomatos',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'Diced Onions',
                u'unit': u'cup',
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'Diced Jalepeno',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': u'tsp',
                u'name': u'Salt',
                u'unit': None,
                u'quantity': None
            },
            {
                u'comment': None,
                u'other': None,
                u'name': u'tsp Pepper',
                u'unit': None,
                u'quantity': None
            },
        ]
        self.mock_ingredient_parser.side_effect = parsed_ingredients
        self.assertEqual(
            html_parse.parse(
                {
                    'url':
                    'http://yourfriendsj.com/recipes/pico-de-gallo-salsa/',
                    'referer': 'http://yourfriendsj.com/recipes/',
                },
                _read_test_file(
                    'yourfriendsj-com_recipes_pico-de-gallo-salsa.html'),
                'http://mock.ingredient.parser'),
            {
                'title':
                u'Quick Pico de Gallo Salsa',
                'url':
                'http://yourfriendsj.com/recipes/pico-de-gallo-salsa/',
                'category':
                'condiment',
                'ingredients': [
                    u'Roma Tomatos', u'Diced Onions', u'Diced Jalepeno',
                    u'Salt', u'tsp Pepper'
                ],
                'mainImage':
                u'http://yourfriendsj.com/wp-content/uploads/2017/08/File_005.jpeg',
                'publishedTime':
                '2017-08-24T00:00:00+00:00',
            })
        self.assertEqual(
            [call[0][0]
             for call in self.mock_ingredient_parser.call_args_list], [
                 u'8 Roma Tomatos', u'\xbd cup Diced Onions',
                 u'1 Diced Jalepeno', u'2 tsp Salt', u'1 tsp Pepper'
             ])
