# tests/test_models.py
import sys
import os
from sqlalchemy.sql import delete
from datetime import datetime, timezone

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models import Session, Learner, Word, Lesson, lesson_words
import pytest

@pytest.fixture
def db_session():
    session = Session()
    # Start a transaction to isolate test changes
    session.begin_nested()
    yield session
    # Rollback changes after each test to avoid persisting test data
    session.rollback()
    session.close()

def test_learner_creation(db_session):
    # Clear learners to avoid conflicts (optional, but safe)
    db_session.query(Learner).delete()
    db_session.commit()
    
    learner = Learner(name="TestUser", target_language="Spanish")
    db_session.add(learner)
    db_session.commit()
    assert learner.id is not None

def test_relationships(db_session):
    # Clear relevant tables to avoid UNIQUE constraint issues
    db_session.execute(delete(lesson_words))  # Clear join table
    db_session.query(Word).delete()
    db_session.query(Lesson).delete()
    db_session.commit()
    
    word = Word(term="test_word", translation="test_translation")  # Unique term
    lesson = Lesson(title="Test Lesson")
    lesson.words.append(word)
    db_session.add(lesson)
    db_session.commit()
    assert len(lesson.words) == 1