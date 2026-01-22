import pytest
from page_loader.naming import format_name, format_dir_name

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

