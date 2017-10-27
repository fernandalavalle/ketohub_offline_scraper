from dateutil import parser
import pytz


def find_image(response):
    return response.xpath(
        '/html/head/meta[@property="og:image"]/@content').extract_first()


def find_published_time(response):
    published_time = response.xpath(
        '/html/head/meta[@property="article:published_time"]/@content'
    ).extract_first()
    if not published_time:
        return None
    return parser.parse(published_time).astimezone(pytz.utc)
