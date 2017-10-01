#!/usr/bin/python2

import argparse
import json
import os

import html_parse


def main(args):
    parsed = {}
    for recipe_key in os.listdir(args.input_root):
        metadata_path = os.path.join(args.input_root, recipe_key,
                                     'metadata.json')
        with open(metadata_path) as metadata_file:
            metadata = json.load(metadata_file)

        html_path = os.path.join(args.input_root, recipe_key, 'index.html')
        raw_html = open(html_path).read()
        parsed[recipe_key] = html_parse.parse(metadata['url'], raw_html)
    print json.dumps(parsed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='KetoHub Offline HTML Scraper',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_root')
    main(parser.parse_args())
