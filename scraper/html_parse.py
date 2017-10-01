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
        'category': 'entree',
    }
