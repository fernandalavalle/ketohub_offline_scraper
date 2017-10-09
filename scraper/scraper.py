#!/usr/bin/python2

import argparse
import json
import logging
import os

import html_parse

logger = logging.getLogger(__name__)


def configure_logging():
    root_logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-15s %(levelname)-4s %(message)s',
        '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)


def main(args):
    configure_logging()
    parsed = {}
    for root in args.input_root:
        for recipe_key in os.listdir(root):
            logging.info('parsing %s', recipe_key)
            if not os.path.exists(os.path.join(root, recipe_key, 'main.jpg')):
                logger.warning(
                    'skipping %s because main image is not available',
                    recipe_key)
                continue
            metadata_path = os.path.join(root, recipe_key, 'metadata.json')
            with open(metadata_path) as metadata_file:
                metadata = json.load(metadata_file)

            html_path = os.path.join(root, recipe_key, 'index.html')
            raw_html = open(html_path).read()
            try:
                parsed[recipe_key] = html_parse.parse(metadata, raw_html)
            except Exception as ex:
                logging.error('Failed to parse %s: %s', recipe_key, ex)
                raise
    logging.info('Parsed %d successfully', len(parsed))
    print json.dumps(parsed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='KetoHub Offline HTML Scraper',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_root', default=[], action='append')
    main(parser.parse_args())
