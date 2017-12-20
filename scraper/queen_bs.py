from common import opengraph
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
    return ingredients_raw


def parse_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()
