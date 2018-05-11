import json
import urllib2

from common import errors


class IngredientParserApiError(errors.ParseError):
    pass


def parse(ingredient_raw, url):

    request = urllib2.Request(
        url=url,
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
            (ingredient_raw, e))

    return json.loads(response.read())
