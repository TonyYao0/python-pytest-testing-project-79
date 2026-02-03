import pytest
import requests
from pathlib import Path
from page_loader import download
import subprocess

def test_download_resource_404(requests_mock, tmp_path, caplog):
    url = "http://ru.hexlet.io/courses.html"
    bad_img_url = "http://ru.hexlet.io/assets/404.png"
    good_img_url = "http://ru.hexlet.io/assets/good.png"
    html_content = (
        '<html><body>'
        '<img src="/assets/404.png">'
        '<img src="/assets/good.png">'
        '</body></html>'
    )
    requests_mock.get(url, text=html_content)
    requests_mock.get(bad_img_url, status_code=404)
    requests_mock.get(good_img_url, text='image data')

    with caplog.at_level("WARNING"):
        actual_path = Path(download(url, tmp_path))

    assert any(record.levelname == 'WARNING' and '404' in record.message 
        for record in caplog.records)
    
    assert "404" in caplog.text
    assert "404.png" in caplog.text

    assert actual_path.name == "ru-hexlet-io-courses.html"
    content = actual_path.read_text()
    assert '/assets/404.png' in content
    assert (
        'ru-hexlet-io-courses_files/ru-hexlet-io-assets-404.png' not in content
    )

    res_dir = tmp_path / "ru-hexlet-io-courses_files"
    assert not (res_dir / "ru-hexlet-io-assets-404.png").exists()
    assert (res_dir / "ru-hexlet-io-assets-good.png").exists()
    assert len(list(res_dir.iterdir())) == 1


def test_download_404_error(requests_mock, tmp_path):
    url = 'http://example.com/404'
    requests_mock.get(url, status_code=404)
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        download(url, tmp_path)
    assert excinfo.value.response.status_code == 404
    items = list(tmp_path.glob('*'))
    assert len(items) == 0, f"Expected no files, but found: {items}"
    assert not any(Path(tmp_path).iterdir())


def test_download_500_error(requests_mock, tmp_path):
    url = 'http://example.com/server-error'
    requests_mock.get(url, status_code=500)
    with pytest.raises(requests.exceptions.HTTPError) as excinfo:
        download(url, tmp_path)
    assert excinfo.value.response.status_code == 500
    assert not list(tmp_path.iterdir())


def test_cli_404_error(tmp_path):
    url = "https://httpbin.org/status/404"
    result = subprocess.run(
        ['page-loader', '--output', str(tmp_path), url],
        capture_output=True,
        text=True
    )
    assert result.returncode == 1
    assert len(result.stderr) > 0
    assert "404" in result.stderr or "Network error" in result.stderr

def test_no_empty_dir_on_fail(requests_mock, tmp_path):
    url = "https://site.com"
    requests_mock.get(url, status_code=500)
    with pytest.raises(Exception):
        download(url, tmp_path)
    items = [x.name for x in tmp_path.iterdir()]
    assert not any(item.endswith('_files') for item in items)

def test_download_network_error(requests_mock, tmp_path):
    url = "https://httpbin.org/status/404"
    requests_mock.get(url, status_code=404)
    with pytest.raises(requests.exceptions.HTTPError):
        download(url, tmp_path)
    assert not any(Path(tmp_path).iterdir())


def test_download_directory_not_found(requests_mock):
    url = "http://ru.hexlet.io/courses.html"
    requests_mock.get(url, text="content")
    with pytest.raises((FileNotFoundError, PermissionError)):
        download(url, "/non/existing/path")


def test_download_permission_denied(requests_mock):
    url = "http://ru.hexlet.io/courses.html"
    requests_mock.get(url, text="content")
    with pytest.raises((PermissionError, OSError)):
        download(url, "/sys")


def test_download_connection_error(requests_mock, tmp_path):
    url = "https://non-existent-site.com"
    requests_mock.get(url, exc=requests.exceptions.ConnectionError)
    with pytest.raises(requests.exceptions.ConnectionError):
        download(url, tmp_path)
    assert not any(Path(tmp_path).iterdir())

def test_download_empty_html(requests_mock, tmp_path):
    url = "https://example.com/empty"
    requests_mock.get(url, text="") 
    
    actual_path = Path(download(url, tmp_path))
    assert actual_path.exists()
    assert actual_path.read_text() == ""


def test_download_tags_without_src(requests_mock, tmp_path):
    url = "https://example.com/no-src"
    html = (
        '<html><body><img src="/valid.png">'
        '<img><script></script></body></html>'
        )
    
    requests_mock.get(url, text=html)
    requests_mock.get("https://example.com/valid.png", text="png")
    
    actual_path = Path(download(url, tmp_path))
    assert actual_path.exists()


def test_download_external_resources(requests_mock, tmp_path):
    url = "https://site.com"
    external_url = "https://cdn.com"
    html = f'<html><link href="{external_url}"></html>'
    requests_mock.get(url, text=html)
    actual_path = Path(download(url, tmp_path))
    content = actual_path.read_text()
    assert external_url in content

def test_download_duplicate_resources(requests_mock, tmp_path):
    url = "https://site.com"
    img_url = "https://site.com/image.png"
    html = '<html><img src="/image.png"><img src="/image.png"></html>'
    requests_mock.get(url, text=html)
    requests_mock.get(img_url, text="data")
    download(url, tmp_path)
    assert requests_mock.call_count == 2

def test_download_protocol_relative_links(requests_mock, tmp_path):
    main_url = 'https://site.com'
    relative_js_path = '//site.com/script.js'
    full_js_url = 'https://site.com/script.js'
    html_content = f'<html><script src="{relative_js_path}"></script></html>'
    requests_mock.get(main_url, text=html_content)
    requests_mock.get(full_js_url, text="console.log('hello')")
    download(main_url, tmp_path)
    res_dir = Path(tmp_path) / "site-com_files"
    expected_js_file = res_dir / "site-com-script.js"
    assert expected_js_file.exists(), f"Файл {expected_js_file} не был скачан"
    assert "hello" in expected_js_file.read_text()
