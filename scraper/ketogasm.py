import logging
import re

from common import opengraph
from common import recipe_schema
import ingredients
import titles

logger = logging.getLogger(__name__)


def parse_title(response, _=None):
    title_raw = ''.join(
        response.xpath('//h1[@class="entry-title"]//text()').extract()).strip()
    title_stripped = _strip_title_tags(title_raw)
    title_stripped = re.sub(u'\u2013$', '', title_stripped).strip()
    return titles.canonicalize(title_stripped)


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
    schema = recipe_schema.read(response)
    ingredients_raw = schema['recipeIngredient']
    ingredients_parsed = [ingredients.parse(i) for i in ingredients_raw]
    # Remove empty ingredients.
    ingredients_parsed = [r for r in ingredients_parsed if r]
    return ingredients_parsed


def parse_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()


def _strip_title_tags(title_raw):
    title_stripped = title_raw.strip()
    title_stripped = re.sub(r'\[.*\]', '', title_stripped).strip()
    title_stripped = re.sub(r'\|.*', '', title_stripped).strip()
    parts = re.split(u'[\u2013:]', title_stripped)
    if len(parts) == 1:
        return title_stripped
    tag_part = parts[-1].strip()
    tags_stripped = re.sub((r'(and)|(Low(-|\s)Carb)|(Gluten(-|\s)Free)|(Keto)'
                            r'|(Dairy(-|\s)Free)|(Sugar(-|\s)Free)|[^A-Za-z]'),
                           '', tag_part)
    if not tags_stripped:
        return parts[0]
    return title_stripped


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
