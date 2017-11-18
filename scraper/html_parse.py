import urlparse

from scrapy import http

import hey_keto_mama
import keto_size_me
import ketoconnect
import ketogasm
import ketovangelist_kitchen
import queen_bs
import ruled_me


def parse(metadata, html):
    # Reconstruct the scrapy response from HTML.
    response = http.TextResponse(url=metadata['url'], body=html)
    domain = _parse_domain(metadata['url'])

    parser_map = {
        'heyketomama.com': hey_keto_mama,
        'ketosizeme.com': keto_size_me,
        'ketoconnect.net': ketoconnect,
        'ketogasm.com': ketogasm,
        'ketovangelistkitchen.com': ketovangelist_kitchen,
        'queenbsincredibleedibles.com': queen_bs,
        'ruled.me': ruled_me,
    }

    if domain not in parser_map:
        raise ValueError('Unexpected domain: %s' % domain)

    parser = parser_map[domain]

    return {
        'url': metadata['url'],
        'title': parser.parse_title(response, metadata),
        'category': parser.parse_category(response, metadata),
        'mainImage': parser.parse_image(response, metadata),
        'ingredients': parser.parse_ingredients(response, metadata),
        'publishedTime': parser.parse_published_time(response, metadata),
    }


def _parse_domain(url):
    domain_parts = urlparse.urlparse(url).netloc.split('.')
    return '.'.join(domain_parts[-2:])
