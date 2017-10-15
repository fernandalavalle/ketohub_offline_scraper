import urlparse

from scrapy import http

import ketoconnect
import ruled_me


def parse(metadata, html):
    # Reconstruct the scrapy response from HTML.
    response = http.TextResponse(url=metadata['url'], body=html)
    domain = _parse_domain(metadata['url'])

    if domain == 'ruled.me':
        parse_recipe = ruled_me.parse_recipe
    elif domain == 'ketoconnect.net':
        parse_recipe = ketoconnect.parse_recipe
    else:
        raise ValueError('Unexpected domain: %s' % domain)

    return parse_recipe(metadata, response)


def _parse_domain(url):
    domain_parts = urlparse.urlparse(url).netloc.split('.')
    return '.'.join(domain_parts[-2:])
