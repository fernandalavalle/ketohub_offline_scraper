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

        self.mock_ingredient_parser = mock.Mock(side_effect=[
            u'fake parsed ingredient 1', u'fake parsed ingredient 2'
        ])
        parser_patch = mock.patch.object(html_parse.ingredients.Parser, 'parse',
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
                    'ingredients': [  # yapf: disable
                        u'fake parsed ingredient 1',
                        u'fake parsed ingredient 2'
                    ],
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
                    'ingredients': [  # yapf: disable
                        u'fake parsed ingredient 1',
                        u'fake parsed ingredient 2'
                    ],
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
                    'ingredients': [  # yapf: disable
                        u'fake parsed ingredient 1',
                        u'fake parsed ingredient 2'
                    ],
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

        self.iterator = 1

        def mock_parse():
            next_ingredient = u'fake parsed ingredient %d' % self.iterator
            self.iterator += 1
            return next_ingredient

        self.mock_ingredient_parser = mock.Mock(
            side_effect=lambda x: mock_parse())
        parser_patch = mock.patch.object(html_parse.ingredients.Parser, 'parse',
                                         self.mock_ingredient_parser)
        self.addCleanup(parser_patch.stop)
        parser_patch.start()

    def test_scrapes_hey_keto_mama_recipe(self):
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
                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3',
                    u'fake parsed ingredient 4',
                    u'fake parsed ingredient 5',
                    u'fake parsed ingredient 6',
                    u'fake parsed ingredient 7',
                    u'fake parsed ingredient 8',
                    u'fake parsed ingredient 9',
                    u'fake parsed ingredient 10',
                    u'fake parsed ingredient 11',
                    u'fake parsed ingredient 12',
                    u'fake parsed ingredient 13',
                    u'fake parsed ingredient 14'
                ],
                'mainImage':
                'https://www.heyketomama.com/wp-content/uploads/2017/10/keto-white-chicken-chili-sm.png',
                'publishedTime':
                '2017-10-30T01:02:11+00:00',
            })

        self.mock_ingredient_parser.assert_has_calls([
            mock.call(u'1 lb chicken'),
            mock.call(u'1.5 cups chicken broth'),
            mock.call(u'2 garlic cloves, finely minced'),
            mock.call(u'1 4.5oz can chopped green chiles'),
            mock.call(u'1 diced jalapeno'),
            mock.call(u'1 diced green pepper'),
            mock.call(u'1/4 cup diced onion'),
            mock.call(u'4 tbsp butter'),
            mock.call(u'1/4 cup heavy whipping cream'),
            mock.call(u'4 oz cream cheese'),
            mock.call(u'2 tsp cumin'),
            mock.call(u'1 tsp oregano'),
            mock.call(u'1/4 tsp cayenne (optional)'),
            mock.call(u'Salt and Pepper to taste')
        ])

    def test_scrapes_ketoconnect_recipe(self):
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
                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3',
                    u'fake parsed ingredient 4',
                    u'fake parsed ingredient 5',
                    u'fake parsed ingredient 6',
                    u'fake parsed ingredient 7',
                    u'fake parsed ingredient 8',
                    u'fake parsed ingredient 9',
                    u'fake parsed ingredient 10',
                    u'fake parsed ingredient 11',
                    u'fake parsed ingredient 12'
                ],
                'mainImage':
                u'https://ketoconnect-apjirmx5iktkd7.netdna-ssl.com/wp-content/uploads/2017/10/low-carb-pizza-crust-slice-flat.jpg',
                'publishedTime':
                '2017-10-08T09:52:09+00:00',
            })

        self.mock_ingredient_parser.assert_has_calls([
            mock.call(u'Coconut flour'),
            mock.call(u'psyilium husk powder'),
            mock.call(u'active dry yeast'),
            mock.call(u'Baking powder'),
            mock.call(u'salt'),
            mock.call(u'olive oil'),
            mock.call(u'Water'),
            mock.call(u'eggs'),
            mock.call(u'minced garlic'),
            mock.call(u'Red Pepper Flakes'),
            mock.call(u'dried minced onion flakes'),
            mock.call(u'Oregano')
        ])

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
                      'ruled_me-charred-veggie-fried-goat-cheese-salad.html'),
                  'http://mock.ingredient.parser'),
            {
                'title':
                'Charred Veggie and Fried Goat Cheese Salad',
                'url':
                'https://www.ruled.me/charred-veggie-fried-goat-cheese-salad/',
                'category':
                'entree',
                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3',
                    u'fake parsed ingredient 4',
                    u'fake parsed ingredient 5',
                    u'fake parsed ingredient 6',
                    u'fake parsed ingredient 7',
                    u'fake parsed ingredient 8',
                    u'fake parsed ingredient 9'
                ],
                'mainImage':
                'https://cdn4.ruled.me/wp-content/uploads/2017/09/fried-goat-cheese-salad-featured.jpg',
                'publishedTime':
                '2017-10-03T11:00:54+00:00',
            })
        self.mock_ingredient_parser.assert_has_calls([
            mock.call(u'2 tablespoons poppy seeds'),
            mock.call(u'2 tablespoons sesame seeds'),
            mock.call(u'1 teaspoon onion flakes'),
            mock.call(u'1 teaspoon garlic flakes'),
            mock.call(u'4 ounces goat cheese'),
            mock.call(u'1 medium (119 g) red bell pepper'),
            mock.call(u'\xbd cup sliced baby portobello mushrooms'),
            mock.call(u'4 cups (80 g) arugula'),
            mock.call(u'1 tablespoon avocado oil')
        ])

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
                  ), 'http://mock.ingredient.parser'),
            {
                'title':
                'Smoked Pork Spare Ribs and Chili Garlic Sauce',
                'url':
                'https://ketogasm.com/smoked-pork-spare-ribs-chili-garlic-recipe/',
                'category':
                'entree',
                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3',
                    u'fake parsed ingredient 4',
                    u'fake parsed ingredient 5',
                    u'fake parsed ingredient 6',
                    u'fake parsed ingredient 7',
                    u'fake parsed ingredient 8',
                    u'fake parsed ingredient 9',
                    u'fake parsed ingredient 10',
                    u'fake parsed ingredient 11'
                ],
                'mainImage':
                'https://ketogasm.com/wp-content/uploads/2017/10/2-smoked-pork-spare-ribs-chili-garlic-sauce.jpg',
                'publishedTime':
                '2017-10-30T12:00:22+00:00',
            })

        self.mock_ingredient_parser.assert_has_calls([
            mock.call(u'6 pounds pork spare ribs'),
            mock.call(u'Hickory wood chips/pellets'),
            mock.call(u'2 tbsp paprika'),
            mock.call(u'2 tbsp salt'),
            mock.call(u'2 tbsp pepper'),
            mock.call(u'1 tsp onion powder'),
            mock.call(u'1 tsp chili powder'),
            mock.call(u'1/2 tsp ground mustard seed'),
            mock.call(u'1/4 cup coconut aminos'),
            mock.call(u'2 tbsp chili garlic sauce'),
            mock.call(u'1 tbsp yellow mustard')
        ])

    def test_scrapes_ketogasm_recipe_with_html_encoded_ingredients(self):
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
                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3',
                    u'fake parsed ingredient 4',
                    u'fake parsed ingredient 5',
                    u'fake parsed ingredient 6',
                    u'fake parsed ingredient 7'
                ],
                'mainImage':
                u'https://cdn1.ketogasm.com/wp-content/uploads/2017/11/1-smoked-sausage-frittata-recipe-spinach-mushroom-low-carb-keto-dairy-free.jpg',
                'publishedTime':
                '2017-11-17T12:00:07+00:00',
            })
        self.mock_ingredient_parser.assert_has_calls([
            mock.call(u'10 oz spinach (raw)'),
            mock.call(u'1 tsp ghee'),
            mock.call(u'4 oz mushrooms (sliced)'),
            mock.call(u'14 oz smoked sausage (uncured, chopped)'),
            mock.call(u'1 clove garlic (minced)'),
            mock.call(u'salt & pepper  (to taste)'),
            mock.call(u'8  eggs')
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
                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3',
                    u'fake parsed ingredient 4',
                    u'fake parsed ingredient 5',
                    u'fake parsed ingredient 6',
                    u'fake parsed ingredient 7',
                    u'fake parsed ingredient 8',
                    u'fake parsed ingredient 9'
                ],
                'mainImage':
                u'https://ketosizeme.com/wp-content/uploads/2015/05/Low-Carb-Keto-Baked-Spaghetti-.jpg',
                'publishedTime':
                '2015-10-20T03:09:44+00:00',
            })
        self.mock_ingredient_parser.assert_has_calls([
            mock.call(u'1 lb Ground Beef (cooked & drained)'),
            mock.call(u'4 cups Spaghetti Squash (cooked)'),
            mock.call(
                u'1 container Wild Oats Organic Tomato Basil Pasta Sauce'),
            mock.call(u'1 1/2 cups Frigo Shredded Parmesan Cheese'),
            mock.call(u'3 1/2 cups Low Moisture Part-skim Mozzarella Cheese'),
            mock.call(u'1 tsp Wild Oats Organic Chili powder'),
            mock.call(u'1/2 tsp Oregano'),
            mock.call(u'2 Garlic Cloves'),
            mock.call(u'1 Large Egg')
        ])

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
                      'ketovangelistkitchen-com_lemon-shortbread-cookies.html'),
                  'http://mock.ingredient.parser'),
            {
                'title':
                u'Lemon Shortbread Cookies',
                'url':
                'http://www.ketovangelistkitchen.com/lemon-shortbread-cookies/',
                'category':
                'dessert',
                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3',
                    u'fake parsed ingredient 4',
                    u'fake parsed ingredient 5',
                    u'fake parsed ingredient 6'
                ],
                'mainImage':
                'http://www.ketovangelistkitchen.com/wp-content/uploads/2016/12/2013-5-27-Lemon-Shortbread-Cookies-7567.jpg',
                'publishedTime':
                '2016-12-19T20:29:38+00:00',
            })
        self.mock_ingredient_parser.assert_has_calls([
            mock.call(u'7 oz. / 200g almond flour (blanched ground almonds)'),
            mock.call(u'1 oz. / 30g chia seeds,\xa0finely ground'),
            mock.call(u'2\xbd oz. / 70g xylitol'),
            mock.call(u'1 tsp. xanthan gum'),
            mock.call(u'Zest of 2 lemons'),
            mock.call(u'3 oz. / 85g cold butter')
        ])

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
                    'ketovangelistkitchen-com_creamy-cucumber-soup.html'),
                'http://mock.ingredient.parser'),
            {
                'title':
                u'Creamy Cucumber Soup',
                'url':
                'http://www.ketovangelistkitchen.com/creamy-cucumber-soup/',
                'category':
                'side',
                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3',
                    u'fake parsed ingredient 4',
                    u'fake parsed ingredient 5',
                    u'fake parsed ingredient 6',
                    u'fake parsed ingredient 7',
                    u'fake parsed ingredient 8',
                    u'fake parsed ingredient 9',
                    u'fake parsed ingredient 10'
                ],
                'mainImage':
                u'http://www.ketovangelistkitchen.com/wp-content/uploads/2017/01/2012-10-19-Creamy-Cucumber-Soup-4907.jpg',
                'publishedTime':
                '2017-01-23T08:15:03+00:00',
            })
        self.mock_ingredient_parser.assert_has_calls([
            mock.call(u'2 TBSP coconut oil or avocado oil'),
            mock.call(u'5 oz. / 140g onion, chopped'),
            mock.call(u'2 \xbd lb / 1120g English cucumbers, chopped'),
            mock.call(
                u'1 \xbd cups / 12 fl oz. unsweetened thin coconut milk (in a carton)'
            ),
            mock.call(u'3 tsp sea salt'),
            mock.call(u'\xbd cup chopped fresh chives'),
            mock.call(u'2 small avocados, skin and pits removed'),
            mock.call(u'2 TBSP heavy cream (double cream)'),
            mock.call(u'1 TBSP white wine'),
            mock.call(u'Chopped green onions (scallions) for garnish')
        ])

    def test_scrapes_low_carb_yum_recipe(self):
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
                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3',
                    u'fake parsed ingredient 4',
                    u'fake parsed ingredient 5',
                    u'fake parsed ingredient 6',
                    u'fake parsed ingredient 7',
                    u'fake parsed ingredient 8',
                    u'fake parsed ingredient 9',
                    u'fake parsed ingredient 10',
                    u'fake parsed ingredient 11',
                    u'fake parsed ingredient 12'
                ],
                'mainImage':
                u'https://lowcarbyum.com/wp-content/uploads/2017/08/baked-sea-scallops-l.jpg',
                'publishedTime':
                '2017-08-11T05:26:46+00:00',
            })

        self.mock_ingredient_parser.assert_has_calls([
            mock.call(
                u'10 pieces sea scallops on the half shell (375g each without shell)'
            ),
            mock.call(u'4 cloves garlic (finely chopped)'),
            mock.call(u'2 tablespoons butter'),
            mock.call(u'1/3 cup cheddar cheese (Freshly Grated)'),
            mock.call(u'3/4 cup mozzarella'),
            mock.call(u'1/3 cup heavy cream'),
            mock.call(u'1/3 cup pork rind'),
            mock.call(u'2  jalape\xf1os (thinly sliced)'),
            mock.call(u'2  lemons (juice and slices)'),
            mock.call(u'salt and black Pepper (to taste)'),
            mock.call(u'fresh parsley for garnishing'),
            mock.call(u'hot water for soaking shells')
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
                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3'
                ],
                'mainImage':
                u'https://lowcarbyum.com/wp-content/uploads/2016/10/low-carb-egg-muffins-wrapped-bacon-sq.jpg',
                'publishedTime':
                '2016-11-19T10:26:25+00:00',
            })
        self.mock_ingredient_parser.assert_has_calls([
            mock.call(u'12 slices of NatureRaised Farms\xae Bacon'),
            mock.call(u'12  large eggs'),
            mock.call(u'8 ounces cheddar cheese (grated)')
        ])

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
                  ), 'http://mock.ingredient.parser'),
            {
                'title':
                u'Dill Pickle Dip',
                'url':
                'http://queenbsincredibleedibles.com/2017/09/19/dill-pickle-dip/',
                'category':
                None,
                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3',
                    u'fake parsed ingredient 4',
                    u'fake parsed ingredient 5',
                    u'fake parsed ingredient 6'
                ],
                'mainImage':
                u'http://queenbsincredibleedibles.com/wp-content/uploads/2017/09/img_6266.jpg',
                'publishedTime':
                '2017-09-19T10:00:46+00:00',
            })
        self.mock_ingredient_parser.assert_has_calls([
            mock.call(u'8 ounces softened cream cheese'),
            mock.call(u'1/4 cup dill pickle juice'),
            mock.call(u'1/4 cup finely chopped pickle'),
            mock.call(
                u'1/2 cup shredded Colby jack cheese, separated in 1/4 cups'),
            mock.call(
                u'1/2 cup crisped bacon \u2013 chopped and separated in 1/4 cups'
            ),
            mock.call(
                u'1/4 cup thinly sliced scallions, plus more for garnish, if desired'
            )
        ])

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
                  ), 'http://mock.ingredient.parser'),
            {
                'title':
                u'The Best Low Carb Gluten-Free Stuffing Ever!',
                'url':
                'http://queenbsincredibleedibles.com/2017/11/03/best-low-carb-gluten-free-stuffing-ever/',
                'category':
                None,
                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3',
                    u'fake parsed ingredient 4',
                    u'fake parsed ingredient 5',
                    u'fake parsed ingredient 6',
                    u'fake parsed ingredient 7',
                    u'fake parsed ingredient 8',
                    u'fake parsed ingredient 9'
                ],
                'mainImage':
                u'http://queenbsincredibleedibles.com/wp-content/uploads/2017/11/img_7054.jpg',
                'publishedTime':
                '2017-11-03T10:00:53+00:00',
            })
        self.mock_ingredient_parser.assert_has_calls([
            mock.call(u'6 cups bread cubes (made with KetoFoccacia)'),
            mock.call(u'1.5 cups chicken stock or turkey stock'),
            mock.call(u'1 tsp fresh rosemary'),
            mock.call(u'1 tsp poultry seasoning'),
            mock.call(u'1 tbsp garlic powder'),
            mock.call(u'1 medium onion'),
            mock.call(u'3 stalks celery'),
            mock.call(u'3 tbsp butter or olive oil'),
            mock.call(u'Salt and pepper')
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

                'ingredients': [  # yapf: disable
                    u'fake parsed ingredient 1',
                    u'fake parsed ingredient 2',
                    u'fake parsed ingredient 3',
                    u'fake parsed ingredient 4',
                    u'fake parsed ingredient 5'
                ],
                'mainImage':
                u'http://yourfriendsj.com/wp-content/uploads/2017/08/File_005.jpeg',
                'publishedTime':
                '2017-08-24T00:00:00+00:00',
            })
        self.mock_ingredient_parser.assert_has_calls([
            mock.call(u'8 Roma Tomatos'),
            mock.call(u'\xbd cup Diced Onions'),
            mock.call(u'1 Diced Jalepeno'),
            mock.call(u'2 tsp Salt'),
            mock.call(u'1 tsp Pepper')
        ])
