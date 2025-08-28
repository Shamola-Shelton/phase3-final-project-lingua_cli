# tests/test_cli.py
import pytest
from click.testing import CliRunner
from lib.cli import cli

@pytest.fixture
def runner():
    return CliRunner()

def test_create_user(runner):
    result = runner.invoke(cli, ['create-user', '--name', 'Test', '--language', 'English'])
    assert result.exit_code == 0
    assert 'Created user' in result.output