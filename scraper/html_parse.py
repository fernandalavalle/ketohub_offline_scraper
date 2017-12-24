import urlparse

from scrapy import http

import hey_keto_mama
import ingredients
import keto_size_me
import ketoconnect
import ketogasm
import ketovangelist_kitchen
import low_carb_yum
import queen_bs
import ruled_me
import titles


def parse(metadata, html):
    # Reconstruct the scrapy response from HTML.
    response = http.TextResponse(url=metadata['url'], body=html)

    scraper = _find_scraper(metadata['url'])

    title = titles.canonicalize(scraper.scrape_title(response, metadata))

    ingredients = _parse_ingredients(
        scraper.scrape_ingredients(response, metadata))

    return {
        'url': metadata['url'],
        'title': title,
        'category': scraper.scrape_category(response, metadata),
        'mainImage': scraper.scrape_image(response, metadata),
        'ingredients': ingredients,
        'publishedTime': scraper.scrape_published_time(response, metadata),
    }


def _find_scraper(url):
    domain = _parse_domain(url)
    try:
        return {
            'heyketomama.com': hey_keto_mama,
            'ketosizeme.com': keto_size_me,
            'ketoconnect.net': ketoconnect,
            'ketogasm.com': ketogasm,
            'ketovangelistkitchen.com': ketovangelist_kitchen,
            'lowcarbyum.com': low_carb_yum,
            'queenbsincredibleedibles.com': queen_bs,
            'ruled.me': ruled_me,
        }[domain]
    except KeyError:
        raise ValueError('Unexpected domain: %s' % domain)


def _parse_ingredients(ingredients_raw):
    ingredients_parsed = [ingredients.parse(i) for i in ingredients_raw]
    # Remove empty ingredients.
    return [p for p in ingredients_parsed if p]


def _parse_domain(url):
    domain_parts = urlparse.urlparse(url).netloc.split('.')
    return '.'.join(domain_parts[-2:])
