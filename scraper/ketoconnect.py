import titles


def parse_recipe(metadata, response):
    title_raw = ''.join(
        response.xpath('//h1[@class="entry-title"]//text()').extract()).strip()
    title = titles.canonicalize(title_raw.split('|')[0].strip())
    category_raw = _category_from_url(metadata['referer'])
    category = _canonicalize_category(category_raw)
    ingredients_list = _parse_ingredients(response)
    return {
        'title': title,
        'url': metadata['url'],
        'category': category,
        'ingredients': ingredients_list
    }


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
