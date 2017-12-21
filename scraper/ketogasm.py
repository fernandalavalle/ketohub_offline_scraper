import titles
import logging
import re

from common import opengraph
from common import recipe_schema

logger = logging.getLogger(__name__)


def parse_title(response, _=None):
    title_raw = ''.join(
        response.xpath('//h1[@class="entry-title"]//text()').extract()).strip()
    title_stripped = _strip_title_tags(title_raw)
    return re.sub(u'\u2013$', '', title_stripped).strip()


def _strip_title_tags(title_raw):
    title_stripped = title_raw.strip()
    title_stripped = re.sub(r'\[.*\]', '', title_stripped).strip()
    title_stripped = re.sub(r'\|.*', '', title_stripped).strip()
    parts = re.split(u'[\u2013:]', title_stripped)
    if len(parts) == 1:
        return title_stripped
    tag_part = parts[-1].strip()
    if titles.is_just_tags(tag_part):
        return parts[0].strip()
    return title_stripped.strip()


def parse_category(response, _=None):
    schema = recipe_schema.read(response)
    category_canonical = None
    try:
        categories = schema['recipeCategory']
    except KeyError:
        logger.warning('No category found')
        return None

    for category in categories:
        category_canonical = _canonicalize_category(category)
        if category_canonical:
            break
    return category_canonical


def parse_image(response, _=None):
    opengraph_url = opengraph.find_image(response)
    if opengraph_url:
        return opengraph_url

    return None


def parse_ingredients(response, _=None):
    return recipe_schema.read(response)['recipeIngredient']


def parse_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()


def _canonicalize_category(category):
    category_map = {
        'Breakfast': 'breakfast',
        'Cocktails': 'beverage',
        'Condiment': 'condiment',
        'Dessert': 'dessert',
        'Dinner': 'entree',
        'Drinks': 'beverage',
        'Lunch': 'entree',
        'Side Dish': 'side',
        'Snacks': 'snack',
    }
    if category not in category_map:
        return None
    return category_map[category]
