import base
import titles


def parse_recipe(metadata, response):
    title = titles.canonicalize(
        response.xpath('//h1//text()').extract_first().strip())
    category_hierarchy = ''.join(
        response.xpath('//div[@class="postCategories"]//text()')
        .extract()).strip()
    category = None
    for category_raw in category_hierarchy.split('>'):
        category_stripped = str(category_raw.strip())
        if category_stripped:
            try:
                category = _canonicalize_category(category_stripped)
            except KeyError:
                continue
            break
    if not category:
        raise base.ParseError('Could not find category for %s -> %s' %
                              (metadata['url'], category_hierarchy))
    return {'title': title, 'url': metadata['url'], 'category': category}


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
