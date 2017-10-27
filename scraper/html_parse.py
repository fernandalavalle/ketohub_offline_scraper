import urlparse

from scrapy import http

import ketoconnect
import ruled_me


def parse(metadata, html):
    # Reconstruct the scrapy response from HTML.
    response = http.TextResponse(url=metadata['url'], body=html)
    domain = _parse_domain(metadata['url'])

    if domain == 'ruled.me':
        parser = ruled_me
    elif domain == 'ketoconnect.net':
        parser = ketoconnect
    else:
        raise ValueError('Unexpected domain: %s' % domain)

    parsed = parser.parse_recipe(metadata, response)
    if domain == 'ketoconnect.net':
        parsed['title'] = parser.parse_title(response, metadata)

    return parsed


def _parse_domain(url):
    domain_parts = urlparse.urlparse(url).netloc.split('.')
    return '.'.join(domain_parts[-2:])
