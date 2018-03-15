import configparser
import io
import os
import shutil
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

import pytest
from giturlparse import parse

from release_exporter import version
from release_exporter.exceptions import ParserError
from release_exporter.utils import get_repo_url_info, date_convert, multi_key_gitlab, description, deprecate, \
    check_version

DUP_SECTION = """\
[branch "v3"]
[travis]
    slug = akshaybabloo/gollahalli-me
[branch "v3"]
    remote = origin
    merge = refs/heads/v3
"""

PASS_SECTION = """\
[remote "origin"]
    url = git@github.com:akshaybabloo/release-exporter.git
    fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
    remote = origin
    merge = refs/heads/master
"""


def temp_file(value):
    temp_location = tempfile.gettempdir()
    os.chdir(temp_location)

    p = Path('.git/')

    if p.is_dir():
        shutil.rmtree(temp_location + os.sep + '.git')

    time.sleep(1)

    os.mkdir('.git/')

    with open(temp_location + os.sep + '.git' + os.sep + 'config', 'w') as config_file:
        config_file.write(value)


# ---------------------- get_repo_url_info ------------------


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
    t = tempfile.gettempdir()
    temp_file(PASS_SECTION)

    content = get_repo_url_info(location=t)

    assert content.owner == 'akshaybabloo'


def test_get_repo_url_info_fail_2():
    t = tempfile.gettempdir()
    temp_file(DUP_SECTION)

    with pytest.raises(configparser.DuplicateSectionError,
                       message='There seems to be a duplicate section in your config. Try giving the repository URL by using --url.'):
        content = get_repo_url_info(location=t)


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


# ---------- deprecation -----------
# Taken from NumPy tests

@deprecate
def old_func(self, x):
    return x


@deprecate(message="Rather use new_func2")
def old_func2(self, x):
    return x


def old_func3(self, x):
    return x


new_func3 = deprecate(old_func3, old_name="old_func3", new_name="new_func3")


def test_deprecate_decorator():
    assert 'deprecated' in old_func.__doc__


def test_deprecate_decorator_message():
    assert 'Rather use new_func2' in old_func2.__doc__


def test_deprecate_fn():
    assert 'old_func3' in new_func3.__doc__
    assert 'new_func3' in new_func3.__doc__


# ------------------- check_version ------------------


class TestCheckVersion(unittest.TestCase):

    @patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_1(self, n, expected_output, mock_stdout):
        request = check_version()
        self.assertIn(expected_output, mock_stdout.getvalue())

    @patch.object(version, '__version__', return_value='1')
    def test_check_version_pass(self, n):
        self.assert_stdout_1('', 'New version')
