import HTMLParser
import re

from common import opengraph
from common import recipe_schema
import titles


def scrape_title(response, _=None):
    title = opengraph.find_title(response)
    title = title.replace(' - YOURFRIENDSJ', '')
    title = re.sub(r'\(.*\)', '', title)
    return _strip_title_tags(title)


def _strip_title_tags(title_raw):
    title_stripped = title_raw.strip()
    parts = re.split(u'[\u2013\\-]', title_stripped)
    if len(parts) == 1:
        return title_stripped
    tag_part = parts[-1].strip()
    if titles.is_just_tags(tag_part):
        return parts[0].strip()
    return title_stripped.strip()


def scrape_category(response, _=None):
    return None


def scrape_image(response, _=None):
    return opengraph.find_image(response)


def scrape_ingredients(response, _=None):
    ingredients_raw = recipe_schema.read(response)['ingredients']
    return _decode_ingredients(ingredients_raw)


def _decode_ingredients(ingredients):
    return [_html_decode(i) for i in ingredients]


def _html_decode(s):
    return HTMLParser.HTMLParser().unescape(s)


def scrape_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()
