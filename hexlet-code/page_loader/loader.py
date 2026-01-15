import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from page_loader.naming import format_name, format_dir_name
def download(url, output_path):
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    base_domain = urlparse(url).netloc
    
    page_file_name = format_name(url)
    dir_name = format_dir_name(url)
    dir_path = os.path.join(output_path, dir_name)

    for img in soup.find_all('img'):
        src = img.get('src')
        if not src:
            continue
            
        full_img_url = urljoin(url, src)
        parsed_img_url = urlparse(full_img_url)
        
        is_local = parsed_img_url.netloc == base_domain
        is_image = parsed_img_url.path.lower().endswith(('.png', '.jpg', '.jpeg'))
        
        if is_local and is_image:
            os.makedirs(dir_path, exist_ok=True)
            
            img_name = format_name(full_img_url)
            img_res = requests.get(full_img_url)
            img_res.raise_for_status()
            
            with open(os.path.join(dir_path, img_name), 'wb') as f:
                f.write(img_res.content)
            
            img['src'] = f"{dir_name}/{img_name}"

    result_path = os.path.join(output_path, page_file_name)
    with open(result_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify(formatter="html5"))
        
    return result_path