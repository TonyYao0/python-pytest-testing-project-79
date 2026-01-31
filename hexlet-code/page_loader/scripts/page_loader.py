import argparse
import sys
from pathlib import Path
from page_loader.loader import download
import logging
import requests


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
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection failed: {e}")
        print("Network error: Failed to connect to host. "
              "Check the URL or your internet connection.", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error: {e}")
        print(f"Network error: {e.response.status_code} "
              f"{e.response.reason} for URL: {args.url}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")
        print(f"File system error: Permission denied. "
              f"No access to '{args.output}'.", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        print(f"File system error: The directory '{args.output}' "
              "does not exist.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
