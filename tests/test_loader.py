from pathlib import Path
import pytest
from page_loader import download
import requests_mock
from bs4 import BeautifulSoup
import difflib

#FIXTURES_PATH = Path('tests/fixtures')


#def get_fixture_path(name):
#    return FIXTURES_PATH / name
def get_fixture_path(name):
    return Path(__file__).parent / 'fixtures' / name

def read_fixture(name, binary=False):
    path = get_fixture_path(name)
    if binary:
        return path.read_bytes()
    return path.read_text(encoding='utf-8')

def html_normalize(html_str):
    soup = BeautifulSoup(html_str, 'html.parser')
    return soup.prettify()

def test_download(requests_mock, tmp_path):
    url = "http://ru.hexlet.io/courses.html"
    courses_url = "http://ru.hexlet.io/courses"
    img_url = "http://ru.hexlet.io/assets/professions/python.png"
    css_url = "http://ru.hexlet.io/assets/application.css"
    runtime_js_url = "https://ru.hexlet.io/packs/js/runtime.js"
    
    before_html = read_fixture('before.html')
    after_html = read_fixture('after.html')
    img_content = read_fixture('python.png', binary=True) 
    css_content = '/* some css */'
    runtime_js_content = "// javascript content"
    
    requests_mock.get(url, text=before_html)
    requests_mock.get(courses_url, text=before_html) 
    requests_mock.get(img_url, content=img_content)
    requests_mock.get(css_url, text=css_content)
    requests_mock.get(runtime_js_url, text=runtime_js_content)
    
    actual_path_str = download(url, tmp_path)
    actual_path = Path(actual_path_str)
    
    actual_html = actual_path.read_text(encoding='utf-8')
    
    normalized_actual = html_normalize(actual_html)
    normalized_expected = html_normalize(after_html)

    diff = difflib.unified_diff(
        normalized_actual.splitlines(),
        normalized_expected.splitlines(),
        fromfile='actual',
        tofile='expected',
        lineterm=''
    )
    diff_output = '\n'.join(diff)
    if diff_output:
        print("Разница в before b after HTML:\n", diff_output)

    assert normalized_actual == normalized_expected

    assets_dir_name = "ru-hexlet-io-courses_files"
    assets_path = tmp_path / assets_dir_name

    assert assets_path.exists() and assets_path.is_dir()

    expected_files = [
        "ru-hexlet-io-assets-professions-python.png",
        "ru-hexlet-io-assets-application.css",
        "ru-hexlet-io-packs-js-runtime.js"
    ]

    for file_name in expected_files:
        file_path = assets_path / file_name
        assert file_path.exists(), f"Файл {file_name} не найден в {assets_dir_name}"
        

        if file_name.endswith('.png'):
            assert file_path.read_bytes() == img_content
        elif file_name.endswith('.css'):
            assert file_path.read_text() == css_content
        elif file_name.endswith('.js'):
            assert file_path.read_text() == runtime_js_content
    
    soup = BeautifulSoup(actual_html, 'html.parser')
    
    external_script = soup.find('script', src="https://js.stripe.com/v3/")
    assert external_script is not None, "Внешний скрипт Stripe должен остаться без изменений"

    external_link = soup.find('link', href="https://cdn2.hexlet.io/assets/menu.css")
    assert external_link is not None, "Внешний CSS должен остаться без изменений"
    assert not (assets_path / "js-stripe-com-v3.js").exists()
