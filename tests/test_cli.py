import os
from unittest.mock import patch

from click.testing import CliRunner

from release_exporter.cli import cli


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
