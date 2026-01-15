import re
import os
from urllib.parse import urlparse

def format_name(url):
    parsed = urlparse(url)
    path = f"{parsed.netloc}{parsed.path}".rstrip('/')
    root, ext = os.path.splitext(path)
    slug = re.sub(r'[^a-zA-Z0-9]', '-', root)
    
    if not ext or ext == '.html':
        return f"{slug}.html"
    
    return f"{slug}{ext}"

def format_dir_name(url):
    parsed = urlparse(url)
    path = f"{parsed.netloc}{parsed.path}".rstrip('/')
    root, _ = os.path.splitext(path)
    slug = re.sub(r'[^a-zA-Z0-9]', '-', root)
    return f"{slug}_files"