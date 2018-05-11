from common import errors
from common import opengraph
from common import recipe_schema


def scrape_title(response, _=None):
    return ''.join(
        response.xpath('//h1[@class="entry-title"]//text()').extract()).strip()


def scrape_category(response, _=None):
    category_raw = opengraph.find_section(response)
    try:
        return _canonicalize_category(category_raw)
    except KeyError:
        raise errors.NoRecipeFoundError(
            'No recipe found. Category is ' + category_raw)


def scrape_image(response, _=None):
    opengraph_url = opengraph.find_image(response)
    if opengraph_url:
        return opengraph_url
    return None


def scrape_ingredients(response, _=None):
    return recipe_schema.read(response)['recipeIngredient']


def scrape_published_time(response, _=None):
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
