import re


extension = ['png', 'jpg', 'jpeg', 'js', 'css']


def format_name(url):
    prepared = re.sub(r'^https?://', '', url).rstrip('/')
    root, sep, ext = prepared.rpartition('.')

    if sep and ext.lower() in extension:
        slug = re.sub(r'[^a-zA-Z0-9]', '-', root)
        return f"{slug}.{ext}"

    base = re.sub(r'\.html$', '', prepared)
    slug = re.sub(r'[^a-zA-Z0-9]', '-', base)
    return f"{slug}.html"


def format_dir_name(url):
    prepared = re.sub(r'^https?://', '', url).rstrip('/')
    base = re.sub(r'\.html$', '', prepared)
    slug = re.sub(r'[^a-zA-Z0-9]', '-', base)
    return f"{slug}_files"
