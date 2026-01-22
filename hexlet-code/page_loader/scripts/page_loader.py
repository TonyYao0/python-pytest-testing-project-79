import argparse
import sys
from pathlib import Path
from page_loader.loader import download

def main():
    parser = argparse.ArgumentParser(description='Page loader')
    parser.add_argument('url')
    parser.add_argument('-o', '--output', default=Path.cwd())
    
    args = parser.parse_args()
    
    try:
        path = download(args.url, args.output)
        print(path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()