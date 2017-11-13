from common import opengraph
import ingredients
import titles


def parse_title(response, _=None):
    title_raw = ''.join(
        response.xpath('//h1[@class="entry-title"]//text()').extract()).strip()
    return titles.canonicalize(title_raw)


def parse_category(_, metadata):
    category_raw = _category_from_url(metadata['referer'])
    return _canonicalize_category(category_raw)


def parse_image(response, _=None):
    opengraph_url = opengraph.find_image(response)
    if opengraph_url:
        return opengraph_url
    return None


def parse_ingredients(response, _=None):
    ingredients_raw = []
    for selector in response.xpath(
            '//strong[contains(text(),"What You Need")]/ancestor::p/following-sibling::ul[1]/li'
    ):
        extracted = selector.xpath('string(self::*)').extract_first()
        ingredients_raw.append(extracted)
    if not ingredients_raw:
        return None
    ingredients_parsed = [ingredients.parse(i) for i in ingredients_raw]
    # Remove empty ingredients.
    ingredients_parsed = [r for r in ingredients_parsed if r]
    return ingredients_parsed


def parse_published_time(response, _=None):
    return opengraph.find_published_time(response).isoformat()


def _category_from_url(url):
    return [str(x) for x in url.split('/') if x][-1]


def _canonicalize_category(category):
    return {
        'appetizers': 'side',
        'sides': 'side',
        'snack': 'snack',
        'soup': 'side',
        'sauces-dressings': 'condiments',
        'fat-bombs': 'dessert',
        'baked-goods': 'dessert',
        'beef': 'entree',
        'chicken-turkey': 'entree',
        'chocolate': 'dessert',
        'fish': 'entree',
        'pork': 'entree',
        'nuts': 'snack',
        'eggs': 'snack',
    }[category.lower()]
