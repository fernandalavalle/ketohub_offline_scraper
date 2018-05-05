import logging
import urlparse

from scrapy import http

from common import errors

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
import your_friends_j

_DEFAULT_GET_SCRAPER_FN = lambda url: _find_scraper(url)

logger = logging.getLogger(__name__)


def parse(metadata, html, get_scraper_fn=_DEFAULT_GET_SCRAPER_FN):
    # Reconstruct the scrapy response from HTML.
    response = http.TextResponse(url=metadata['url'], body=html)

    scraper = get_scraper_fn(metadata['url'])

    title = titles.canonicalize(scraper.scrape_title(response, metadata))

    return {
        'url': metadata['url'],
        'title': title,
        'category': _parse_category(scraper, response, metadata),
        'mainImage': scraper.scrape_image(response, metadata),
        'ingredients': _parse_ingredients(scraper, response, metadata),
        'publishedTime': _parse_published_time(scraper, response, metadata),
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
            'yourfriendsj.com': your_friends_j,
        }[domain]
    except KeyError:
        raise ValueError('Unexpected domain: %s' % domain)


def _parse_category(scraper, response, metadata):
    try:
        return scraper.scrape_category(response, metadata)
    except Exception as e:
        logger.error('Failed to parse category from %s: %s', metadata['url'],
                     e.message)
        return None


def _parse_published_time(scraper, response, metadata):
    try:
        return scraper.scrape_published_time(response, metadata)
    except Exception as e:
        logger.error('Failed to parse published time from %s: %s',
                     metadata['url'], e.message)
        return None


def _parse_ingredients(scraper, response, metadata):
    try:
        ingredients_raw = scraper.scrape_ingredients(response, metadata)
    except errors.NoRecipeFoundError:
        raise
    except Exception as e:
        logger.error('Failed to parse ingredients from %s: %s', metadata['url'],
                     e.message)
        return []
    ingredients_parsed = [ingredients.parse(i) for i in ingredients_raw]
    # Remove empty ingredients.
    return [p for p in ingredients_parsed if p]


def _parse_domain(url):
    domain_parts = urlparse.urlparse(url).netloc.split('.')
    return '.'.join(domain_parts[-2:])
