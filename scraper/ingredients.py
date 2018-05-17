import json
import urllib2

from common import errors


class IngredientParserApiError(errors.ParseError):
    pass


class Parser(object):

    def __init__(self, url):
        self._url = url

    def parse(self, ingredient_raw):
        """Parses a raw text ingredient into just the 'name' of the ingredient.

        Args:
            ingredient_raw: Raw text of an ingredient, for example:
                '1 pound carrots, young ones if possible'

        Returns:
            String of 'name' element of the ingredient, for example:
                'carrots's

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
        except urllib2.HTTPError as e:
            raise IngredientParserApiError(
                'Request to parse ingredient, %s, failed with: %s' %
                (ingredient_raw, e.message))

        return json.loads(response.read())['ingredientParsed']
