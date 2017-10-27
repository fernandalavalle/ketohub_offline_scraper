import os
import unittest

from scrapy import http

from scraper.common import opengraph

class FindImageTest(unittest.TestCase):

    def test_finds_image(self):
        self.assertEqual(
            opengraph.find_image(http.TextResponse("""
<html>
<head>
 <meta property="og:image" content="https://dummy.com/recipe-image.jpg" />
</head>
<body><p>blah</p></body>
</html>""")), 'https://dummy.com/recipe-image.jpg')
