import os
import re
from urllib.parse import urlparse
import requests

def format_name(url):
    parsed_url = urlparse(url)
    combined = parsed_url.netloc + parsed_url.path
    name = re.sub(r'[^a-zA-Z0-9]', '-', combined)
    return f"{name}.html"

def download(url, output_path):
    filename = format_name(url)
    full_path = os.path.join(output_path, filename)
    
    response = requests.get(url)
    response.raise_for_status()
    
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    return full_path