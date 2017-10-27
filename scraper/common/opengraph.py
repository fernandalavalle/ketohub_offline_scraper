def find_image(response):
    return response.xpath(
        '/html/head/meta[@property="og:image"]/@content').extract_first()
