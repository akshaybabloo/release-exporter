import pytest
from giturlparse import parse

from release_exporter.exceptions import ParserError
from release_exporter.utils import get_repo_url_info, date_convert, multi_key_gitlab, description


def test_get_repo_url_info_args():
    content = get_repo_url_info(
        repo_url='https://github.com/akshaybabloo/release-exporter.git')

    assert parse(
        'https://github.com/akshaybabloo/release-exporter.git').owner == content.owner


def test_get_repo_url_info_fail():
    with pytest.raises(ParserError,
                       message='Git config file does not exist please provide the repository url by using --url.'):
        content = get_repo_url_info(location='yo')


def test_get_repo_url_info_pass():
    content = get_repo_url_info()

    assert content.owner == 'akshaybabloo'


# ---------------- date_convert -----------------------


def test_date_convert_fail():
    with pytest.raises(ValueError, message="Unknown string format"):
        content = date_convert('10-10-2019T12:12:12z')


def test_date_convert_pass():
    content = date_convert('10-10-2019')
    assert content == '2019-10-10'


def test_date_convert_pass2():
    content = date_convert('2008-01-14T04:33:35Z')
    assert content == '2008-01-14'


# ----------------- multi_key_gitlab ------------------


def test_multi_key_gitlab_pass():
    data = {
        "owner": {
            "username": "user"
        }
    }

    content = multi_key_gitlab(data)
    assert content == "user"


def test_multi_key_gitlab_pass_except():
    data = {
        "owner": "user"
    }

    content = multi_key_gitlab(data)
    assert content == None


# ------------- description ------------

def test_description_pass():
    provider = "some provider"
    repo_name = "some repo name"
    tags_number = 22

    expected = '\n'.join(['+-----------------+----------------+',
                          '| Provider        | some provider  |',
                          '+-----------------+----------------+',
                          '| Repository Name | some repo name |',
                          '+-----------------+----------------+',
                          '| Number of Tags  | 22             |',
                          '+-----------------+----------------+'])

    actual = description(provider, repo_name, tags_number)

    assert actual == expected


def test_description_fail():
    provider = "some provider"
    repo_name = "some repo name"

    expected = '\n'.join(['+-----------------+----------------+',
                          '| Provider        | some provider  |',
                          '+-----------------+----------------+',
                          '| Repository Name | some repo name |',
                          '+-----------------+----------------+',
                          '| Number of Tags  | 22             |',
                          '+-----------------+----------------+'])

    actual = description(provider, repo_name)

    assert actual != expected
