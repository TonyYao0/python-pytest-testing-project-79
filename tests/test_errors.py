import pytest
import requests
from pathlib import Path
from page_loader import download

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

    assert "404" in caplog.text
    assert "404.png" in caplog.text

    assert actual_path.name == "ru-hexlet-io-courses.html"
    content = actual_path.read_text()
    assert '/assets/404.png' in content

    res_dir = tmp_path / "ru-hexlet-io-courses_files"
    assert not (res_dir / "ru-hexlet-io-assets-404.png").exists()
    assert (res_dir / "ru-hexlet-io-assets-good.png").exists()
    assert len(list(res_dir.iterdir())) == 1


def test_download_network_error(requests_mock, tmp_path):
    url = "https://httpbin.org/status/404"
    requests_mock.get(url, status_code=404)
    with pytest.raises(requests.exceptions.HTTPError):
        download(url, tmp_path)
    assert not any(Path(tmp_path).iterdir()), "Directory should be empty"


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
    assert not any(Path(tmp_path).iterdir()), "Directory should be empty"