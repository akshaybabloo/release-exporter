from click.testing import CliRunner
import pytest
from release_exporter.cli import cli, json, markdown, print_version


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
