from common import opengraph
import ingredients
import titles


def parse_title(response, _=None):
    title_raw = ''.join(
        response.xpath('//h2[contains(@class, "entry-title")]//text()')
        .extract_first()).strip()
    return titles.canonicalize(title_raw)


def parse_category(unused_response, _=None):
    # Queen B's does not maintain any category information.
    return None


def parse_image(response, _=None):
    opengraph_url = opengraph.find_image(response)
    if opengraph_url:
        return opengraph_url
    return None


def parse_ingredients(response, _=None):
    ingredients_raw = []
    for selector in response.xpath(
            '//div[contains(@class, "post-content")]//ul/li'):
        extracted = selector.xpath('string(self::*)').extract_first()
        ingredients_raw.append(extracted)
    if not ingredients_raw:
        return None
    ingredients_parsed = [ingredients.parse(i) for i in ingredients_raw]
    # Remove empty ingredients.
    ingredients_parsed = [r for r in ingredients_parsed if r]
    return ingredients_parsed


def parse_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()
