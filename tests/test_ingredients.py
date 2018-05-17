import io
import json
import mock
import unittest
import urllib2

from scraper import ingredients


class ParseTest(unittest.TestCase):

    def setUp(self):
        self.mock_response = mock.Mock()
        self.mock_urlopen = mock.Mock(return_value=self.mock_response)

        urllib2_patch = mock.patch.object(ingredients.urllib2, 'urlopen',
                                          self.mock_urlopen)
        self.addCleanup(urllib2_patch.stop)
        urllib2_patch.start()

        self.parser = ingredients.Parser('http://mockurl')

    def test_parse_successful_request_returns_flattened_dict(self):
        self.mock_response.read.return_value = json.dumps({
            'ingredientParsed': {
                'name': 'mock ingredient'
            }
        })
        actual = self.parser.parse('mock ingredient')
        self.assertTrue(isinstance(actual, dict))
        self.assertDictEqual(actual, {'name': 'mock ingredient'})

    def test_parse_raises_api_error_when_parser_returns_error_response(self):
        mock_response = io.BytesIO('dummy server error')
        self.mock_urlopen.side_effect = urllib2.HTTPError(
            url='mockurl', code=400, msg=None, hdrs={}, fp=mock_response)

        with self.assertRaises(ingredients.IngredientParserApiError):
            self.parser.parse('mock ingredient')
