from src.cli import cli


def test_cli_group_help(cli_runner):
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert "Commands:" in result.output


def test_cli_version(cli_runner):
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "Expense Tracker CLI, version" in result.output


def test_commands_registered(cli_runner):
    expected_commands = ["add", "update", "delete", "list", "summary", "export", "set-budget", "delete-budget", "view-budget"]
    registered_commands = cli.commands.keys()
    
    # Check that all expected commands are registered
    for command in expected_commands:
        assert command in registered_commands

    # Check that the output of --help contains all expected commands
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    for command in expected_commands:
        assert command in result.output

    # Check that there are no extra commands registered
    for command in registered_commands:
        assert command in expected_commands


def test_invalid_command(cli_runner):
    result = cli_runner.invoke(cli, ["nonexistent"])
    assert result.exit_code != 0
    assert "No such command 'nonexistent'" in result.output
