# tests/test_cli.py
import sys
import os
import pytest
from unittest.mock import patch
from click.testing import CliRunner
from lib.cli import cli
from lib.models import Session, Learner, Word

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def db_session():
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_create_user(runner, db_session):
    result = runner.invoke(cli, ['create-user', '--name', 'Test', '--language', 'English'])
    assert result.exit_code == 0
    assert 'Created user' in result.output
    assert db_session.query(Learner).filter_by(name='Test').first() is not None

def test_login_success(runner, db_session):
    # Setup: Create a user
    learner = Learner(name='TestLogin', target_language='Spanish')
    db_session.add(learner)
    db_session.commit()
    
    result = runner.invoke(cli, ['login', '--name', 'TestLogin'])
    assert result.exit_code == 0
    assert 'Logged in as TestLogin' in result.output

def test_login_fail(runner):
    result = runner.invoke(cli, ['login', '--name', 'NonExistent'])
    assert result.exit_code == 0
    assert 'User not found' in result.output

def test_add_word(runner, db_session):
    result = runner.invoke(cli, ['add-word', '--term', 'test', '--translation', 'prueba'])
    assert result.exit_code == 0
    assert 'Added word: test -> prueba' in result.output
    assert db_session.query(Word).filter_by(term='test').first() is not None

def test_view_progress(runner, db_session):
    # Setup: Create learner and session
    learner = Learner(name='ProgressTest', target_language='Spanish')
    db_session.add(learner)
    db_session.commit()
    learner.add_session(db_session, score=80)
    
    result = runner.invoke(cli, ['view-progress', '--learner_id', learner.id])
    assert result.exit_code == 0
    assert 'Progress for ProgressTest' in result.output

@patch('lib.helpers.get_ai_client')
def test_quiz_vocab(mock_get_ai_client, runner, db_session):
    # Setup: Create learner
    learner = Learner(name='QuizTest', target_language='Spanish')
    db_session.add(learner)
    db_session.commit()
    
    # Mock AI response
    mock_get_ai_client.return_value = None  # Simulate no API key
    result = runner.invoke(cli, ['quiz-vocab', '--learner_id', learner.id])
    assert result.exit_code == 0
    assert 'AI unavailable' in result.output

@patch('lib.helpers.get_ai_client')
def test_practice_grammar(mock_get_ai_client, runner):
    mock_get_ai_client.return_value = None
    result = runner.invoke(cli, ['practice-grammar', '--sentence', 'Hola como estas', '--language', 'Spanish'])
    assert result.exit_code == 0
    assert 'AI unavailable' in result.output

@patch('lib.helpers.get_ai_client')
def test_simulate_convo(mock_get_ai_client, runner):
    mock_get_ai_client.return_value = None
    result = runner.invoke(cli, ['simulate-convo', '--language', 'Spanish'], input='Hello\nexit\n')
    assert result.exit_code == 0
    assert 'AI unavailable' in result.output