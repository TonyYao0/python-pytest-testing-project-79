import os
import requests_mock
from page_loader import download

def test_download(tmp_path):
    url = "https://ru.hexlet.io/courses"
    expected_name = "ru-hexlet-io-courses.html"
    
    with requests_mock.Mocker() as m:
        m.get(url, text="content")
        result_path = download(url, tmp_path)
        
        assert result_path == os.path.join(tmp_path, expected_name)
        assert os.path.exists(result_path)
        with open(result_path, 'r') as f:
            assert f.read() == "content"