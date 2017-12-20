from common import errors
from common import opengraph
from common import recipe_schema
import titles


def parse_title(response, _=None):
    title_raw = ''.join(
        response.xpath('//h1[@class="entry-title"]//text()').extract()).strip()
    return titles.canonicalize(title_raw)


def parse_category(response, _=None):
    category_raw = opengraph.find_section(response)
    try:
        return _canonicalize_category(category_raw)
    except KeyError:
        raise errors.NoRecipeFoundError('No recipe found. Category is ' +
                                        category_raw)


def parse_image(response, _=None):
    opengraph_url = opengraph.find_image(response)
    if opengraph_url:
        return opengraph_url
    return None


def parse_ingredients(response, _=None):
    schema = recipe_schema.read(response)
    return schema['recipeIngredient']


def parse_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()


def _canonicalize_category(category):
    return {
        'Keto Breakfast Recipes': 'breakfast',
        'Keto Lunch Recipes': 'entree',
        'Keto Dinner Recipes': 'entree',
        'Keto Side Dish Recipes': 'side',
        'Keto Crock Pot Recipes': 'entree',
        'Keto Snack Recipes': 'snack',
        'Keto Sauce & Dip Recipes': 'condiment',
        'Keto Fat Bomb Recipes': 'dessert',
        'Keto Dessert Recipes': 'dessert',
        'Keto Holiday Recipes': 'dessert',
    }[category]
