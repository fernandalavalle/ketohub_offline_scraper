from common import opengraph
from common import recipe_schema
import titles


def parse_title(response, _=None):
    return titles.canonicalize(
        opengraph.find_title(response).replace(' - Hey Keto Mama', ''))


def parse_category(_, metadata):
    return None


def parse_image(response, _=None):
    return opengraph.find_image(response)


def parse_ingredients(response, _=None):
    return recipe_schema.read(response)['recipeIngredient']


def parse_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()
