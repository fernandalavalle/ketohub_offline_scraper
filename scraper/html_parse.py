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

    parser = _Parser(scraper, response, metadata)

    return {
        'url': metadata['url'],
        'title': parser.parse_title(),
        'category': parser.parse_category(),
        'mainImage': parser.parse_main_image(),
        'ingredients': parser.parse_ingredients(),
        'publishedTime': parser.parse_published_time(),
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


def _parse_domain(url):
    domain_parts = urlparse.urlparse(url).netloc.split('.')
    return '.'.join(domain_parts[-2:])


class _Parser(object):

    def __init__(self, scraper, response, metadata):
        self._scraper = scraper
        self._response = response
        self._metadata = metadata

    def parse_title(self):
        title_raw = self._scraper.scrape_title(self._response, self._metadata)
        if not title_raw:
            raise errors.NoRecipeFoundError(
                'Failed to scrape required field: title for %s' %
                self._metadata['url'])
        title_canonicalized = titles.canonicalize(title_raw)
        if not title_canonicalized:
            raise errors.NoRecipeFoundError(
                'Failed to scrape required field: title for %s' %
                self._metadata['url'])
        return title_canonicalized

    def parse_category(self):
        try:
            return self._scraper.scrape_category(self._response, self._metadata)
        except Exception as e:
            logger.error('Failed to parse category from %s: %s',
                         self._metadata['url'], e.message)
            return None

    def parse_main_image(self):
        main_image = self._scraper.scrape_image(self._response, self._metadata)
        if not main_image:
            raise errors.NoRecipeFoundError(
                'Failed to scrape required field: mainImage for %s' %
                self._metadata['url'])
        return main_image

    def parse_published_time(self):
        try:
            return self._scraper.scrape_published_time(self._response,
                                                       self._metadata)
        except Exception as e:
            logger.error('Failed to parse published time from %s: %s',
                         self._metadata['url'], e.message)
            return None

    def parse_ingredients(self):
        try:
            ingredients_raw = self._scraper.scrape_ingredients(
                self._response, self._metadata)
        except errors.NoRecipeFoundError:
            raise
        except Exception as e:
            logger.error('Failed to parse ingredients from %s: %s',
                         self._metadata['url'], e.message)
            return []
        ingredients_parsed = [ingredients.parse(i) for i in ingredients_raw]
        # Remove empty ingredients.
        return [p for p in ingredients_parsed if p]
