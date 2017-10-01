from scrapy import http


def parse(url, html):
    # Reconstruct the scrapy response from HTML.
    response = http.TextResponse(url=url, body=html)
    if url.find('ruled.me') >= 0:
        return _parse_ruled_me_response(url, response)
    else:
        return _parse_ketoconnect_response(url, response)


def _parse_ruled_me_response(url, response):
    pass


def _parse_ketoconnect_response(url, response):
    title_raw = ''.join(response.xpath('//h1//text()').extract()).strip()
    title = title_raw.split('|')[0].strip()
    return {
        'title': title,
        'url': url,
        'category': _find_ketoconnect_category(url)
    }


# Hack workaround until we can automatically deduce categories for KetoConnect.
def _find_ketoconnect_category(url):
    return {
        'https://www.ketoconnect.net/recipe/apple-pork-chops/':
        'entree',
        'https://www.ketoconnect.net/recipe/cauliflower-waffles/':
        'entree',
        'https://www.ketoconnect.net/recipe/keto-butter-chicken/':
        'entree',
        'https://www.ketoconnect.net/recipe/easy-chicken-enchilada-casserole/':
        'entree',
        'https://www.ketoconnect.net/recipe/oven-baked-fish/':
        'entree',
        'https://www.ketoconnect.net/recipe/cauliflower-salad/':
        'side',
        'https://www.ketoconnect.net/recipe/coconut-flour-bread/':
        'side',
        'https://www.ketoconnect.net/recipe/cured-egg-yolk/':
        'side',
        'https://www.ketoconnect.net/recipe/zucchini-gratin/':
        'side',
        'https://www.ketoconnect.net/recipe/spicy-cilantro-dressing/':
        'side',
        'https://www.ketoconnect.net/recipe/low-carb-tortillas/':
        'side',
        'https://www.ketoconnect.net/recipe/gluten-free-sugar-free-cookies/':
        'breakfast',
        'https://www.ketoconnect.net/recipe/low-carb-waffles/':
        'breakfast',
        'https://www.ketoconnect.net/recipe/healthy-lemon-poppy-seed-muffins/':
        'breakfast',
        'https://www.ketoconnect.net/recipe/low-carb-breakfast-casserole/':
        'breakfast',
        'https://www.ketoconnect.net/recipe/low-carb-cereal/':
        'breakfast',
        'https://www.ketoconnect.net/recipe/french-omelette/':
        'breakfast',
        'https://www.ketoconnect.net/recipe/low-carb-yogurt/':
        'snack',
        'https://www.ketoconnect.net/recipe/homemade-almond-butter/':
        'snack',
        'https://www.ketoconnect.net/recipe/cocoa-roasted-almonds/':
        'snack',
        'https://www.ketoconnect.net/recipe/low-carb-peanut-butter/':
        'snack',
        'https://www.ketoconnect.net/recipe/sugar-free-graham-crackers/':
        'snack',
        'https://www.ketoconnect.net/recipe/sugar-free-donuts/':
        'dessert',
        'https://www.ketoconnect.net/recipe/low-carb-donuts/':
        'dessert',
        'https://www.ketoconnect.net/recipe/keto-bars/':
        'dessert',
        'https://www.ketoconnect.net/recipe/low-carb-smores/':
        'dessert',
        'https://www.ketoconnect.net/recipe/keto-fat-bombs/':
        'dessert',
        'https://www.ketoconnect.net/recipe/pumpkin-spice-latte-recipe/':
        'beverage',
        'https://www.ketoconnect.net/recipe/keto-pre-workout/':
        'beverage',
        'https://www.ketoconnect.net/recipe/low-carb-smoothies/':
        'beverage',
        'https://www.ketoconnect.net/recipe/keto-coffee/':
        'beverage',
        'https://www.ketoconnect.net/recipe/turmeric-tea/':
        'beverage',
        'https://www.ketoconnect.net/recipe/bulletproof-coffee/':
        'beverage',
    }[url]
