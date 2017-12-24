from common import opengraph
from common import recipe_schema


def scrape_title(response, _=None):
    return opengraph.find_title(response).replace(' - Hey Keto Mama', '')


def scrape_category(_, metadata):
    return None


def scrape_image(response, _=None):
    return opengraph.find_image(response)


def scrape_ingredients(response, _=None):
    return recipe_schema.read(response)['recipeIngredient']


def scrape_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()
