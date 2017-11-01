import unittest

from scraper import titles


class TitlesCanonicalizeTest(unittest.TestCase):

    def test_removes_prefixes(self):
        self.assertEqual(
            titles.canonicalize('Keto Bites: Zuchini Pizza'), 'Zuchini Pizza')
        self.assertEqual(
            titles.canonicalize('Keto Recipe: Cheesy Spinach'),
            'Cheesy Spinach')

    def test_enforces_conventions(self):
        self.assertEqual(
            titles.canonicalize('Gluten Free Pizza'), 'Gluten-Free Pizza')
        self.assertEqual(
            titles.canonicalize('Guilt Free Ice Cream'), 'Guilt-Free Ice Cream')
        self.assertEqual(
            titles.canonicalize('Sugar Free Cookies'), 'Sugar-Free Cookies')
        self.assertEqual(
            titles.canonicalize('Chocolate & Hearts'), 'Chocolate and Hearts')
        self.assertEqual(
            titles.canonicalize('Low Carb Moscow Mule Recipe'),
            'Low Carb Moscow Mule')
        # Don't replace ampersand unless it has surrounding spaces
        self.assertEqual(titles.canonicalize('Keto PB&J'), 'Keto PB&J')
        self.assertEqual(
            titles.canonicalize('Beef in a Slow-Cooker'),
            'Beef in a Slow Cooker')

    def test_handles_unicode_characters(self):
        self.assertEqual(
            titles.canonicalize(u'Pumpkin Seed Bark \u2013 Dark Chocolate'),
            u'Pumpkin Seed Bark \u2013 Dark Chocolate')
