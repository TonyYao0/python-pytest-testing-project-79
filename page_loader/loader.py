import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from page_loader.naming import format_name, format_dir_name
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

RESOURCES_TAGS = {
    'img': 'src',
    'link': 'href',
    'script': 'src'
}


def download(url, output_path):

    logger.info(f"Requested URL: {url}")
    logger.info(f"Output path: {output_path}")

    output_dir = Path(output_path)
    if not output_dir.exists() or not output_dir.is_dir():
        raise FileNotFoundError(f"Directory not found: {output_path}")
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    base_domain = urlparse(url).netloc

    page_name = format_name(url)
    dir_name = format_dir_name(url)
    dir_path = output_dir / dir_name

    dir_path.mkdir(exist_ok=True)

    for tag_name, attr in RESOURCES_TAGS.items():
        for tag in soup.find_all(tag_name):
            resource_url = tag.get(attr)
            if not resource_url:
                continue

            full_url = urljoin(url, resource_url)

            if urlparse(full_url).netloc == base_domain:
                resource_name = format_name(full_url)
                resource_path = dir_path / resource_name

                local_resource_link = f"{dir_name}/{resource_name}"

                if resource_path.exists():
                    logger.info(f"Resource '{resource_name}' saved")
                    tag[attr] = local_resource_link
                    continue

                try:
                    res_response = requests.get(full_url)
                    res_response.raise_for_status()

                    resource_path.write_bytes(res_response.content)
                    tag[attr] = local_resource_link
                    logger.info(f"Resource '{resource_name}' saved")
                except requests.RequestException as e:
                    logger.warning(f"Could not download {full_url}: {e}")
                    continue

    result_html_path = output_dir / page_name
    result_html_path.write_text(soup.prettify(), encoding='utf-8')
    logger.info(f"Page saved to {result_html_path}")

    return result_html_path
