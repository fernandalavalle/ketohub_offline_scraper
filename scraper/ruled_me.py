from common import errors
from common import opengraph
import titles


def parse_title(response, _=None):
    return titles.canonicalize(
        response.xpath('//h1//text()').extract_first().strip())


def parse_category(response, _=None):
    category = None
    category_hierarchy = ''.join(
        response.xpath('//div[@class="postCategories"]//text()')
        .extract()).strip()
    for category_raw in category_hierarchy.split('>'):
        category_stripped = str(category_raw.strip())
        if category_stripped:
            try:
                category = _canonicalize_category(category_stripped)
            except KeyError:
                continue
            break
    if not category:
        raise errors.ParseError(
            'Could not find category for %s -> %s' % response.url,
            category_hierarchy)
    return category


def parse_image(response, _=None):
    return opengraph.find_image(response)


def parse_ingredients(response, _=None):
    ingredients_raw = []
    for ingredient_raw in response.xpath('//table//tr/td[1]//text()').extract():
        ingredients_raw.append(ingredient_raw)
    # First row is headers, last two rows are totals and per-serving macros.
    return ingredients_raw[1:-2]


def parse_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()


def _canonicalize_category(category):
    return {
        'breakfast': 'breakfast',
        'lunch': 'entree',
        'dinner': 'entree',
        'dessert': 'dessert',
        'snacks': 'snack',
        'side items': 'side',
        'condiments': 'condiment',
    }[category.lower()]
