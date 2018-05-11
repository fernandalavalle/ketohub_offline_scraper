from dateutil import parser
import pytz
import re

from common import opengraph
from common import recipe_schema


def scrape_title(response, _=None):
    title_raw = ''.join(
        response.xpath('//h1[@class="entry-title"]//text()').extract()).strip()
    return _strip_title_flavor_text(title_raw)


def _strip_title_flavor_text(title):
    return re.sub(r'\s*\|.+$', '', title)


def scrape_category(_, metadata):
    category_raw = _category_from_url(metadata['referer'])
    return _canonicalize_category(category_raw)


def scrape_image(response, _=None):
    opengraph_url = opengraph.find_image(response)
    if opengraph_url:
        return opengraph_url

    for image_url in response.xpath(
            '//div[@id="tve_editor"]//img/@src').extract():
        if image_url.endswith('.jpg'):
            return image_url
    return None


def scrape_ingredients(response, _=None):
    ingredients_raw = []
    for ingredient_raw in response.xpath(
            '//span[@class="wpurp-recipe-ingredient-name"]/text()').extract():
        ingredients_raw.append(ingredient_raw)
    return ingredients_raw


def scrape_published_time(response, _=None):
    schema = recipe_schema.read(response)
    return parser.parse(schema['datePublished']).replace(
        tzinfo=pytz.UTC).isoformat()


def _category_from_url(url):
    return [str(x) for x in url.split('/') if x][-1]


def _canonicalize_category(category):
    return {
        'main-dishes': 'entree',
        'side-dishes': 'side',
        'breakfasts': 'breakfast',
        'snacks': 'snack',
        'desserts': 'dessert',
        'beverages': 'beverage',
    }[category.lower()]
