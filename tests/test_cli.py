import os
import shutil
import tempfile
import time
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from release_exporter.cli import cli
from release_exporter.exceptions import UnknownRepo


class Values:

    def __init__(self):
        self.token = 123
        self.url = 123
        self.location = 123
        self.version = 123

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)


SECTION = """\
[remote "origin"]
    url = git@gollahalli.com:akshaybabloo/release-exporter.git
    fetch = +refs/heads/*:refs/remotes/origin/*
[branch "master"]
    remote = origin
    merge = refs/heads/master
"""

GITLAB_SECTION = """\
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


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])

    assert result.exit_code == 0
    assert 'help' in result.output


def test_print_version():
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])

    assert result.exit_code == 0
    assert isinstance(result.output, str)


def test_markdown_fail():
    runner = CliRunner()
    result = runner.invoke(cli, ['--token', 'some_token', 'markdown'], obj=Values())

    assert result.exit_code == -1
    assert isinstance(result.exception, KeyError)


def test_json_fail():
    runner = CliRunner()
    result = runner.invoke(cli, ['--token', 'some_token', 'json'], obj=Values())

    assert result.exit_code == -1
    assert isinstance(result.exception, KeyError)


@patch('os.name', 'nt')
def test_markdown_fail_2():
    runner = CliRunner()
    result = runner.invoke(cli, ['--token', 'some_token', '--location', os.getcwd(), 'markdown'], obj=Values())

    assert result.exit_code == -1
    assert isinstance(result.exception, KeyError)


@patch('os.name', 'nt')
def test_json_fail_2():
    runner = CliRunner()
    result = runner.invoke(cli, ['--token', 'some_token', '--location', os.getcwd(), 'json'], obj=Values())

    assert result.exit_code == -1
    assert isinstance(result.exception, KeyError)

t = tempfile.gettempdir()
    temp_file(SECTION)

@patch('os.name', 'nt')
def test_markdown_exception():

    runner = CliRunner()
    result = runner.invoke(cli, ['--token', 'some_token', '--location', t, 'markdown'], obj=Values())

    assert result.exit_code == -1
    assert isinstance(result.exception, UnknownRepo)


def test_json_fail_exception():

    runner = CliRunner()
    result = runner.invoke(cli, ['--token', 'some_token', '--location', t, 'json'], obj=Values())

    assert result.exit_code == -1
    assert isinstance(result.exception, UnknownRepo)


def test_markdown_fail_3():
    t = tempfile.gettempdir()
    temp_file(GITLAB_SECTION)

    runner = CliRunner()
    result = runner.invoke(cli, ['--token', 'some_token', '--location', t, 'markdown'], obj=Values())

    assert result.exit_code == -1
    assert isinstance(result.exception, KeyError)


def test_json_fail_3():
    t = tempfile.gettempdir()
    temp_file(GITLAB_SECTION)

    runner = CliRunner()
    result = runner.invoke(cli, ['--token', 'some_token', '--location', t, 'json'], obj=Values())

    assert result.exit_code == -1
    assert isinstance(result.exception, KeyError)
