from common import opengraph
from common import recipe_schema
import ingredients
import titles


def parse_title(response, _=None):
    return titles.canonicalize(
        opengraph.find_title(response).replace(' - Hey Keto Mama', ''))


def parse_category(_, metadata):
    return None


def parse_image(response, _=None):
    return opengraph.find_image(response)


def parse_ingredients(response, _=None):
    schema = recipe_schema.read(response)
    ingredients_raw = schema['recipeIngredient']
    ingredients_parsed = [ingredients.parse(i) for i in ingredients_raw]
    # Remove empty ingredients.
    ingredients_parsed = [r for r in ingredients_parsed if r]
    return ingredients_parsed


def parse_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()
