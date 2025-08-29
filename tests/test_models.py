# tests/test_models.py
import sys
import os
import uuid
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from lib.models import Session, Learner, Word, Lesson, PracticeSession

@pytest.fixture
def db_session():
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_learner_creation(db_session):
    unique_name = f"TestUser_{uuid.uuid4().hex[:8]}"
    learner = Learner(name=unique_name, password="testpass", target_language="Spanish")
    db_session.add(learner)
    db_session.commit()
    assert learner.id is not None
    db_session.delete(learner)
    db_session.commit()

def test_relationships(db_session):
    unique_term = f"test_{uuid.uuid4().hex[:8]}"
    word = Word(term=unique_term, translation="test")
    lesson = Lesson(title="Test Lesson")
    lesson.words.append(word)
    db_session.add(lesson)
    db_session.commit()
    assert len(lesson.words) == 1
    db_session.delete(word)
    db_session.delete(lesson)
    db_session.commit()

def test_learner_oop_features(db_session):
    unique_name = f"OOPTest_{uuid.uuid4().hex[:8]}"
    learner = Learner(name=unique_name, password="testpass", target_language="Spanish")
    db_session.add(learner)
    db_session.commit()
    learner.add_session(db_session, score=95)
    assert learner.proficiency_level == 'Advanced'
    assert learner.fluency_score > 0
    assert "advanced quiz" in learner.generate_quiz_prompt()
    # Delete sessions first to avoid NOT NULL constraint
    db_session.query(PracticeSession).filter_by(learner_id=learner.id).delete()
    db_session.delete(learner)
    db_session.commit()