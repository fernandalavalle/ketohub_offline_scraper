# Defines common utilities that many scrapers need.


class Error(Exception):
    pass


class ParseError(Error):
    pass


def find_opengraph_image(response):
    return response.xpath(
        '/html/head/meta[@property="og:image"]/@content').extract_first()
