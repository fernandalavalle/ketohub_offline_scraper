import json
import mock
import unittest
import urllib2

from scraper import ingredients


class MockHttpError(urllib2.HTTPError):

    def __init__(self):
        self.code = 'mock code'
        self.msg = 'mock msg'


class MockUrlError(urllib2.URLError):

    def __init__(self):
        self.reason = 'mock reason'


class ParseIngredientTest(unittest.TestCase):

    def setUp(self):
        self.mock_response = mock.Mock()
        self.mock_urlopen = mock.Mock(return_value=self.mock_response)

        urllib2_patch = mock.patch.object(ingredients.urllib2, 'urlopen',
                                          self.mock_urlopen)
        self.addCleanup(urllib2_patch.stop)
        urllib2_patch.start()

    def test_parse_successful_request_returns_dictionary(self):
        self.mock_response.read.return_value = json.dumps({
            "name":
            "mock ingredient"
        })
        self.assertTrue(
            isinstance(
                ingredients.parse('mock ingredient', 'http://mockurl'), dict))

    def test_parse_raises_api_error_when_parser_returns_error_response(self):
        self.mock_urlopen.side_effect = MockHttpError()
        with self.assertRaises(ingredients.IngredientParserApiError):
            ingredients.parse('mock ingredient', 'http://mockurl')

    def test_parse_raises_api_error_when_ingredient_parser_cannot_be_reached(
            self):
        self.mock_urlopen.side_effect = MockUrlError()
        with self.assertRaises(ingredients.IngredientParserApiError):
            ingredients.parse('mock ingredient', 'http://mockurl')
