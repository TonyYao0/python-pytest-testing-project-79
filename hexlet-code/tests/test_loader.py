import os
import pytest
from page_loader import download

def test_download_images(requests_mock, tmp_path):
    url = "http://ru.hexlet.io/courses.html"
    img_url = "http://ru.hexlet.io/assets/professions/python.png"
    
    requests_mock.get(url, text='<html><body><img src="/assets/professions/python.png"></body></html>')
    requests_mock.get(img_url, content=b"png_data")
    
    result_path = download(url, str(tmp_path))
    
    assert os.path.basename(result_path) == "ru-hexlet-io-courses.html"
    
    expected_img_path = os.path.join(
        str(tmp_path), 
        "ru-hexlet-io-courses_files", 
        "ru-hexlet-io-assets-professions-python.png"
    )
    assert os.path.exists(expected_img_path)