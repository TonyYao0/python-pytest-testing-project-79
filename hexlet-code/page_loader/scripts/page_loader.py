import argparse
import sys
from pathlib import Path
from page_loader.loader import download
import logging


def main():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url')
    parser.add_argument(
        '-o', '--output',
        default=Path.cwd(),
        help='output directory (default: current working directory)'
        )

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    try:
        path = download(args.url, args.output)
        print(path)
    except Exception as e:
        logging.error(f'An error occurred: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
