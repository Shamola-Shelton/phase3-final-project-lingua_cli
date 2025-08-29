# tests/test_integration.py
import sys
import os
import uuid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from lib.cli import new_user, add_word, view_progress, quiz_vocab, export_flashcards, current_user_id
from lib.models import Session, Learner, Word
from lib.helpers import call_ai

@pytest.fixture
def db_session():
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_basic_flow(db_session):
    # Create user
    unique_name = f"IntTest_{uuid.uuid4().hex[:8]}"
    with patch('click.prompt') as mock_prompt, patch('getpass.getpass') as mock_getpass:
        mock_prompt.side_effect = [unique_name, 'English']
        mock_getpass.return_value = 'intpass'
        new_user()

    learner = db_session.query(Learner).filter_by(name=unique_name).first()
    assert learner is not None

    # Set user ID
    global current_user_id
    current_user_id = learner.id

    # Add word
    unique_term = "testword"
    with patch('click.prompt') as mock_prompt:
        mock_prompt.side_effect = [unique_term, 'prueba', 'r']
        add_word()

    # View progress
    with patch('click.prompt') as mock_prompt:
        mock_prompt.return_value = 'r'
        view_progress()

    # Mock AI quiz
    with patch('lib.helpers.call_ai') as mock_ai, patch('click.prompt') as mock_prompt:
        mock_ai.return_value = "1. Question: What? Answer: This\n2. Question: Who? Answer: That"
        mock_prompt.side_effect = ['This', 'That', 'r']
        quiz_vocab()

    # Export flashcards
    with patch('click.prompt') as mock_prompt:
        mock_prompt.return_value = 'r'
        export_flashcards()

    # Cleanup
    session = Session()
    word = session.query(Word).filter_by(term=unique_term).first()
    if word:
        session.delete(word)
    learner = session.query(Learner).filter_by(name=unique_name).first()
    if learner:
        session.delete(learner)
    session.commit()
    session.close()
    current_user_id = None