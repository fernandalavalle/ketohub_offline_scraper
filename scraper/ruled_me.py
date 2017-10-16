import base
import ingredients
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
    ingredients_list = _parse_ingredients(response)
    main_image = base.find_opengraph_image(response)
    return {
        'title': title,
        'url': metadata['url'],
        'category': category,
        'ingredients': ingredients_list,
        'mainImage': main_image,
    }


def _parse_ingredients(response):
    ingredients_raw = []
    for ingredient_raw in response.xpath('//table//tr/td[1]//text()').extract():
        ingredients_raw.append(ingredient_raw)
    # First row is headers, last two rows are totals and per-serving macros.
    ingredients_raw = ingredients_raw[1:-2]
    ingredients_parsed = [ingredients.parse(i) for i in ingredients_raw]
    # Remove empty ingredients.
    ingredients_parsed = [r for r in ingredients_parsed if r]
    return ingredients_parsed


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
