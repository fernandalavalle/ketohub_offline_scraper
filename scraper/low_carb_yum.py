import re

from common import opengraph
from common import recipe_schema
import titles


def parse_title(response, _=None):
    title = opengraph.find_title(response).replace(' | Low Carb Yum', '')
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


def parse_category(response, _=None):
    category_raw = ''.join(
        response.xpath('//p[@class="entry-meta"]/a//text()').extract()).strip()
    return _canonicalize_category(category_raw)


def _canonicalize_category(category_raw):
    return {
        'appetizers': 'appetizer',
        'beverages': 'beverage',
        'breakfast': 'breakfast',
        'bagels': 'breakfast',
        'breads': 'side',
        'savory breads': 'side',
        'desserts': 'dessert',
        'frozen desserts': 'dessert',
        'cakes': 'dessert',
        'cheesecakes': 'dessert',
        'cookies & bars': 'dessert',
        'candies': 'dessert',
        'pies': 'dessert',
        'main dishes': 'entree',
        'side dishes': 'side',
        'snacks': 'snack',
        'muffins': 'snack',
        'beef': 'entree',
        'chicken': 'entree',
        'ham': 'entree',
        'turkey': 'entree',
        'pork': 'entree',
        'casseroles': 'entree',
        'soups': 'entree',
        'salads': 'entree',
        'vegetable': 'entree',
        'instant pot': 'entree',
        'miscellaneous': 'entree',
        'eggs': 'breakfast',
        'beans (legumes)': 'side',
        'sauces & spreads': 'condiments',
    }[category_raw.lower()]


def parse_image(response, _=None):
    return opengraph.find_image(response)


def parse_ingredients(response, _=None):
    return recipe_schema.read(response)['recipeIngredient']


def parse_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()
