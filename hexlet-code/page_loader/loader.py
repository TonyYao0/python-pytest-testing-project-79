import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from page_loader.naming import format_name, format_dir_name
from pathlib import Path

RESOURCES_TAGS = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}

def download(url, output_path):
    output_dir = Path(output_path)
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    base_domain = urlparse(url).netloc

    page_name = format_name(url)
    dir_name = format_dir_name(url)
    dir_path = output_dir / dir_name

    resources_dir = output_dir / dir_name
    resources_dir.mkdir(parents=True, exist_ok=True)

    for tag_name, attr in RESOURCES_TAGS.items():
        for tag in soup.find_all(tag_name):
            resource_url = tag.get(attr)
            if not resource_url:
                continue

            full_url = urljoin(url, resource_url)

            if urlparse(full_url).netloc == base_domain:
                resource_name = format_name(full_url)
                resource_path = dir_path / resource_name

                try:
                    res_response = requests.get(full_url)
                    res_response.raise_for_status()
                    resource_path.write_bytes(res_response.content)
                    tag[attr] = f"{dir_name}/{resource_name}"
                except requests.RequestException as e:
                    print(f"Error downloading {full_url}: {e}")
                    continue

                tag[attr] = f"{dir_name}/{resource_name}"

    result_html_path = output_dir / page_name
    result_html_path.write_text(soup.prettify(), encoding='utf-8')

    return result_html_path