from common import opengraph
from common import recipe_schema
import ingredients
import titles


def parse_title(response, _=None):
    title_raw = ''.join(
        response.xpath('//h1[@class="entry-title"]//text()').extract()).strip()
    return titles.canonicalize(title_raw.split('[Recipe]')[0].strip())


def parse_category(response, _=None):
    schema = recipe_schema.read(response)
    category_canonical = None
    for category in schema['recipeCategory']:
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
