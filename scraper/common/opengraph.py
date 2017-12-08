from dateutil import parser
import pytz


def find_title(response):
    return response.xpath(
        '//meta[@property="og:title"]/@content').extract_first()


def find_image(response):
    return response.xpath(
        '//meta[@property="og:image"]/@content').extract_first()


def find_published_time(response):
    published_time = response.xpath(
        '//meta[@property="article:published_time"]/@content').extract_first()
    if not published_time:
        return None
    return parser.parse(published_time).astimezone(pytz.utc)


def find_section(response):
    return response.xpath(
        '//meta[@property="article:section"]/@content').extract_first()
