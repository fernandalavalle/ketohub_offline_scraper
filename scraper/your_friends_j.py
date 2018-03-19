import HTMLParser
import logging
import re

from dateutil import parser
import pytz

from common import opengraph
from common import recipe_schema
import titles

logger = logging.getLogger(__name__)


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
    category_url = _get_category_url(response)
    category = _category_from_url(category_url)
    return _normalize_category(category)


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
    date_raw = recipe_schema.read(response)['datePublished']
    return parser.parse(date_raw).replace(tzinfo=pytz.utc).isoformat()


def _get_category_url(response):
    return recipe_schema.read(response)['recipeCategory']


def _category_from_url(url):
    return url.split('/')[-2]


def _normalize_category(category):
    try:
        return {
            'desserts': 'dessert',
            'dips-sauces': 'condiment',
            'entree': 'entree',
            'meat': 'entree',
            'quick-break': 'side',
        }[category]
    except KeyError:
        logger.info('Unexpected category: %s', category)
        return None
