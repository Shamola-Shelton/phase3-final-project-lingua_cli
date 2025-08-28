# tests/test_integration.py
import pytest
from unittest.mock import patch
from click.testing import CliRunner
from lib.cli import cli, initial_menu
from lib.models import Session, Learner, Word

runner = CliRunner()

@pytest.fixture
def db_session():
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_full_flow(db_session):
    # Create user
    result = runner.invoke(cli, ['create-user', '--name', 'IntTest', '--language', 'English'])
    assert 'Created user' in result.output
    learner = db_session.query(Learner).filter_by(name='IntTest').first()
    assert learner is not None

    # Login (simulate via function, not CLI, due to getpass)
    global current_user
    from lib.cli import current_user
    learner = db_session.query(Learner).filter_by(name='IntTest').first()
    current_user = learner

    # Add word
    result = runner.invoke(cli, ['add-word', '--term', 'test', '--translation', 'prueba'])
    assert 'Added word' in result.output

    # View progress
    result = runner.invoke(cli, ['view-progress'])
    assert 'Progress for IntTest' in result.output

    # Mock AI quiz
    with patch('lib.helpers.call_ai') as mock_ai:
        mock_ai.return_value = "Question: What? \nAnswer: This\n"
        result = runner.invoke(cli, ['quiz-vocab'])
        assert 'Score' in result.output

    # Export
    result = runner.invoke(cli, ['export-flashcards'])
    assert 'Exported' in result.output

    # Logout
    result = runner.invoke(cli, ['logout'])
    assert 'Logged out' in result.output