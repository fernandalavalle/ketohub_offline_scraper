import json

from common import errors
from common import opengraph
import ingredients
import titles


def parse_title(response, _=None):
    title_raw = ''.join(
        response.xpath('//h1[@class="entry-title"]//text()').extract()).strip()
    return titles.canonicalize(title_raw.split('[Recipe]')[0].strip())


def parse_category(response, _=None):
    recipe_schema = _read_recipe_schema(response)
    category_canonical = None
    try:
        for category in recipe_schema['recipeCategory']:
            category_canonical = _canonicalize_category(category)
            if category_canonical:
                break
    except KeyError:
        raise errors.NoRecipeFoundError('Could not find recipe category')
    return category_canonical


def parse_image(response, _=None):
    opengraph_url = opengraph.find_image(response)
    if opengraph_url:
        return opengraph_url

    return None


def parse_ingredients(response, _=None):
    recipe_schema = _read_recipe_schema(response)
    try:
        ingredients_raw = recipe_schema['recipeIngredient']
    except KeyError:
        raise errors.RecipeNotFoundError('Could not find recipe ingredients')
    ingredients_parsed = [ingredients.parse(i) for i in ingredients_raw]
    # Remove empty ingredients.
    ingredients_parsed = [r for r in ingredients_parsed if r]
    return ingredients_parsed


def parse_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()


def _read_recipe_schema(response):
    recipe_schema_raw = response.xpath(
        '//script[@type="application/ld+json"]/text()').extract()[-1]
    return json.loads(recipe_schema_raw)


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
