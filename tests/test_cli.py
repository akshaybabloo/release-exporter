from click.testing import CliRunner
import pytest
from release_exporter.cli import cli, json, markdown


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])

    assert result.exit_code == 0
    assert 'help' in result.output
