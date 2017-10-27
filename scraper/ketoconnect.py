from common import opengraph
import titles


def parse_recipe(metadata, response):
    ingredients_list = _parse_ingredients(response)
    main_image = _find_main_image_url(response)
    return {
        'url': metadata['url'],
        'ingredients': ingredients_list,
        'mainImage': main_image,
    }


def parse_title(response, _=None):
    title_raw = ''.join(
        response.xpath('//h1[@class="entry-title"]//text()').extract()).strip()
    return titles.canonicalize(title_raw.split('|')[0].strip())


def parse_category(_, metadata):
    category_raw = _category_from_url(metadata['referer'])
    return _canonicalize_category(category_raw)


def _category_from_url(url):
    return [str(x) for x in url.split('/') if x][-1]


def _parse_ingredients(response):
    ingredients_raw = []
    for ingredient_raw in response.xpath(
            '//span[@class="wpurp-recipe-ingredient-name"]/text()').extract():
        ingredients_raw.append(ingredient_raw)
    return ingredients_raw


def _canonicalize_category(category):
    return {
        'main-dishes': 'entree',
        'side-dishes': 'side',
        'breakfasts': 'breakfast',
        'snacks': 'snack',
        'desserts': 'dessert',
        'beverages': 'beverage',
    }[category.lower()]


def _find_main_image_url(response):
    opengraph_url = opengraph.find_image(response)
    if opengraph_url:
        return opengraph_url

    for image_url in response.xpath(
            '//div[@id="tve_editor"]//img/@src').extract():
        if image_url.endswith('.jpg'):
            return image_url
    return None
