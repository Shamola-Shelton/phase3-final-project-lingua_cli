# tests/test_models.py
import pytest
from lib.models import Session, Learner, Word, Lesson

@pytest.fixture
def db_session():
    session = Session()
    yield session
    session.close()

def test_learner_creation(db_session):
    learner = Learner(name="TestUser", target_language="Spanish")
    db_session.add(learner)
    db_session.commit()
    assert learner.id is not None

def test_relationships(db_session):
    word = Word(term="test", translation="test")
    lesson = Lesson(title="Test Lesson")
    lesson.words.append(word)
    db_session.add(lesson)
    db_session.commit()
    assert len(lesson.words) == 1