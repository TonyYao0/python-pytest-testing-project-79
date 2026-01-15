import os
import pytest
from page_loader import download
import requests_mock
from page_loader.naming import format_name, format_dir_name

FIXTURES_PATH = 'tests/fixtures'

def get_fixture_path(name):
    return os.path.join(FIXTURES_PATH, name)

def read_fixture(name, mode='r'):
    with open(get_fixture_path(name), mode) as f:
        return f.read()

def test_download(requests_mock, tmp_path):
    url = "http://ru.hexlet.io/courses.html"
    img_url = "http://ru.hexlet.io/assets/professions/python.png"
    
    before_html = read_fixture('before.html')
    expected_after_html = read_fixture('after.html')
    img_content = read_fixture('python.png', mode='rb') 
    
    requests_mock.get(url, text=before_html)
    requests_mock.get(img_url, content=img_content)
    
    actual_path = download(url, str(tmp_path))
    
    with open(actual_path, 'r') as f:
        assert f.read().strip() == expected_after_html.strip()
    
    expected_img_path = os.path.join(
        str(tmp_path), 
        'ru-hexlet-io-courses_files', 
        'ru-hexlet-io-assets-professions-python.png'
    )
    assert os.path.exists(expected_img_path)

@pytest.mark.parametrize("url, expected_name", [
    ("https://ru.hexlet.io", "ru-hexlet-io.html"),
    ("ru.hexlet.io.courses", "ru-hexlet-io-courses.html"),
    ("ru.hexlet.io.courses.html", "ru-hexlet-io-courses.html"),
    ("https://ru.hexlet.io.assets.professions.python.png", "ru-hexlet-io-assets-professions-python.png"),
    ("ru.hexlet.io", "ru-hexlet-io.html"),
    ("ru.hexlet.io.courses/", "ru-hexlet-io-courses.html"),
])
def test_format_name(url, expected_name):
    assert format_name(url) == expected_name

@pytest.mark.parametrize("url, expected_dir", [
    ("https://ru.hexlet.io", "ru-hexlet-io_files"),
    ("ru.hexlet.io.courses", "ru-hexlet-io-courses_files"),
    ("ru.hexlet.io.courses.html", "ru-hexlet-io-courses_files"),
])

def test_format_dir_name(url, expected_dir):
    assert format_dir_name(url) == expected_dir

