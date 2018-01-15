from release_exporter.utils import *
from release_exporter.exceptions import ParserError
from giturlparse import parse
import pytest


def test_get_repo_url_info_args():
    content = get_repo_url_info(repo_url='https://github.com/akshaybabloo/release-exporter.git')

    assert parse('https://github.com/akshaybabloo/release-exporter.git').owner == content.owner


def test_get_repo_url_info_fail():
    with pytest.raises(ParserError,
                       message='Git config file does not exist please provide the repository url by using --url.'):
        content = get_repo_url_info(location='yo')


def test_get_repo_url_info_pass():
    content = get_repo_url_info()

    assert content.owner == 'akshaybabloo'
