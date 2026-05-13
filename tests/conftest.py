import os
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://johnmakarov.github.io/egor-xlsx-example/")


@pytest.fixture
def download_file_from(tmp_path_factory, page):
    def _download(selector: str) -> Path:
        with page.expect_download() as download_info:
            page.click(selector)

        download = download_info.value
        save_path = tmp_path_factory.mktemp("session") / download.suggested_filename
        download.save_as(save_path)
        return save_path

    return _download
