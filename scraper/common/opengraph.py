from dateutil import parser

class Error(Exception):
    pass


class ParseError(Error):
    pass


def find_image(response):
    return response.xpath(
        '/html/head/meta[@property="og:image"]/@content').extract_first()


def find_published_time(response):
    publish_time_str = response.xpath(
        '/html/head/meta[@property="og:published_time"]/@content').extract_first()
    if not publish_time_str:
        return None
    return parser.parse(publish_time_str).astimezone(pytz.utc)
