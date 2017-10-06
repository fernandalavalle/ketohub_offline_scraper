from scrapy import http


class Error(Exception):
    pass


class ParseError(Error):
    pass


def parse(metadata, html):
    # Reconstruct the scrapy response from HTML.
    response = http.TextResponse(url=metadata['url'], body=html)
    if metadata['url'].find('ruled.me') >= 0:
        return _parse_ruled_me_response(metadata, response)
    else:
        return _parse_ketoconnect_response(metadata, response)


def _parse_ruled_me_response(metadata, response):
    title = response.xpath('//h1//text()').extract_first().strip()
    category_hierarchy = ''.join(
        response.xpath('//div[@class="postCategories"]//text()')
        .extract()).strip()
    category = None
    for category_raw in category_hierarchy.split('>'):
        category_stripped = str(category_raw.strip())
        if category_stripped:
            try:
                category = _canonicalize_ruled_me_category(category_stripped)
            except KeyError:
                continue
            break
    if not category:
        raise ParseError('Could not find category for %s -> %s' %
                         (metadata['url'], category_hierarchy))
    return {'title': title, 'url': metadata['url'], 'category': category}


def _parse_ketoconnect_response(metadata, response):
    title_raw = ''.join(response.xpath('//h1//text()').extract()).strip()
    title = title_raw.split('|')[0].strip()
    category_raw = _ketoconnect_category_from_url(metadata['referer'])
    category = _canonicalize_ketoconnect_category(category_raw)
    return {'title': title, 'url': metadata['url'], 'category': category}


def _ketoconnect_category_from_url(url):
    return [str(x) for x in url.split('/') if x][-1]


def _canonicalize_ketoconnect_category(category):
    return {
        'main-dishes': 'entree',
        'side-dishes': 'side',
        'breakfasts': 'breakfast',
        'snacks': 'snack',
        'desserts': 'dessert',
        'beverages': 'beverage',
    }[category.lower()]


def _canonicalize_ruled_me_category(category):
    return {
        'breakfast': 'breakfast',
        'lunch': 'entree',
        'dinner': 'entree',
        'dessert': 'dessert',
        'snacks': 'snack',
        'side items': 'side',
        'condiments': 'condiment',
    }[category.lower()]
