import pytest
from click.testing import CliRunner
from src.cli import cli


@pytest.fixture
def runner():
    """Fixture to run the CLI commands."""
    return CliRunner()


def test_cli_group_help(runner):
    """Test that the CLI help is displayed correctly."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert "Commands:" in result.output


def test_cli_version(runner):
    """Test that the CLI version is displayed correctly."""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "Expense Tracker CLI, version" in result.output


def test_commands_registered(runner):
    """Test that the main commands are registered in the CLI."""
    commands = ["add", "update", "delete", "list", "summary", "export", "set-budget", "delete-budget", "budget"]
    result = runner.invoke(cli, ["--help"])
    for command in commands:
        assert command in result.output


def test_invalid_command(runner):
    """Test that an invalid command generates the expected error."""
    result = runner.invoke(cli, ["nonexistent"])
    assert result.exit_code != 0
    assert "No such command 'nonexistent'" in result.output
