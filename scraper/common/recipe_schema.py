import json

import errors


def read(response):
    for raw_json in response.xpath(
            '//script[@type="application/ld+json"]/text()').extract():
        json_dict = json.loads(raw_json)
        if '@type' in json_dict and json_dict['@type'] == 'Recipe':
            return json_dict

    raise errors.NoRecipeFound('Response does not contain a Recipe schema')


