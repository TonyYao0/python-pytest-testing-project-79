import pytest
import requests
from pathlib import Path
from page_loader import download

def test_download_resource_404(requests_mock, tmp_path):
    url = "http://ru.hexlet.io/courses.html"
    bad_img_url = "http://ru.hexlet.io/assets/404.png"
    html_content = '<html><body><img src="/assets/404.png"></body></html>'
    requests_mock.get(url, text=html_content)
    requests_mock.get(bad_img_url, status_code=404)
    actual_path = Path(download(url, tmp_path))
    assert actual_path.name == "ru-hexlet-io-courses.html"
    content = actual_path.read_text()
    assert '/assets/404.png' in content
    assert 'ru-hexlet-io_files/ru-hexlet-io-assets-404.png' not in content
    res_path = tmp_path / "ru-hexlet-io-courses_files" / "ru-hexlet-io-assets-404.png"
    assert not res_path.exists()

def test_download_network_error(requests_mock, tmp_path):
    url = "https://httpbin.org"
    requests_mock.get(url, status_code=404)
    with pytest.raises(requests.exceptions.HTTPError):
        download(url, tmp_path)

def test_download_directory_not_found(requests_mock):
    url = "http://ru.hexlet.io/courses.html"
    requests_mock.get(url, text="content")
    with pytest.raises((FileNotFoundError, PermissionError)):
        download(url, "/non/existing/path")

def test_download_permission_denied(requests_mock, tmp_path):
    url = "http://ru.hexlet.io/courses.html"
    requests_mock.get(url, text="content")
    tmp_path.chmod(0o444)
    with pytest.raises(PermissionError):
        download(url, str(tmp_path))

def test_download_connection_error(requests_mock, tmp_path):
    url = "https://non-existent-site.com"
    requests_mock.get(url, exc=requests.exceptions.ConnectionError)
    with pytest.raises(requests.exceptions.ConnectionError):
        download(url, tmp_path)