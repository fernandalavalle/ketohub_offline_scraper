import json
import urllib2

from common import errors


class IngredientParserApiError(errors.ParseError):
    pass


class IngredientParser(object):

    def __init__(self, url):
        self._url = url

    def parse(self, ingredient_raw):
        """Parses a raw text ingredient into an ingredient json object.

        Args:
            ingredient_raw: Raw text of an ingredient, for example:
                '1 pound carrots, young ones if possible'

        Returns:
            A parsed ingredient, for example:
                 {
                   "ingredientParsed":{
                      "comment":"young ones if possible",
                      "name":"carrots",
                      "quantity":1.0,
                      "unit":"pound"
                   }
                }

        Raises:
            IngredientParserApiError: An error occurred accessing the ingredient
                parser API.
        """

        request = urllib2.Request(
            url=self._url,
            data=json.dumps({
                'ingredient': ingredient_raw
            }),
            headers={'Content-Type': 'application/json'})

        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError as e:
            raise IngredientParserApiError(
                'Unable to reach ingredient parser: %s' % e)
        except urllib2.HTTPError as e:
            raise IngredientParserApiError(
                'Request to parse ingredient, %s, failed with: %s' %
                (ingredient_raw, e.message))

        return json.loads(response.read())['ingredientParsed']
