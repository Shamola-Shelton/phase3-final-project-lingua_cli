# tests/test_cli.py
import sys
import os
import uuid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from lib.cli import new_user, add_word, current_user_id
from lib.models import Session, Learner, Word

@pytest.fixture
def db_session():
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_new_user(db_session):
    unique_name = f"TestNew_{uuid.uuid4().hex[:8]}"
    with patch('click.prompt') as mock_prompt, patch('getpass.getpass') as mock_getpass:
        mock_prompt.side_effect = [unique_name, 'English']
        mock_getpass.return_value = 'testpass'
        new_user()
    learner = db_session.query(Learner).filter_by(name=unique_name).first()
    assert learner is not None
    db_session.delete(learner)
    db_session.commit()

def test_add_word(db_session):
    global current_user_id
    unique_name = f"TestAdd_{uuid.uuid4().hex[:8]}"
    learner = Learner(name=unique_name, password="testpass", target_language="Spanish")
    db_session.add(learner)
    db_session.commit()
    current_user_id = learner.id
    db_session.close()

    unique_term = "testword"
    with patch('click.prompt') as mock_prompt:
        mock_prompt.side_effect = [unique_term, 'friend', 'r']
        add_word()

    session = Session()
    word = session.query(Word).filter_by(term=unique_term).first()
    assert word is not None
    session.delete(word)
    learner = session.query(Learner).filter_by(name=unique_name).first()
    if learner:
        session.delete(learner)
        session.commit()
    session.close()
    current_user_id = None