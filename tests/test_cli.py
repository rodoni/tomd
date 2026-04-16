import pytest
from click.testing import CliRunner
from tomd.cli import cli

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert "tomd - Document to Markdown Converter" in result.output

def test_convert_invalid_path():
    runner = CliRunner()
    result = runner.invoke(cli, ['convert', 'non_existent_file.txt'])
    assert result.exit_code != 0
    assert "Invalid value for 'PATH'" in result.output
