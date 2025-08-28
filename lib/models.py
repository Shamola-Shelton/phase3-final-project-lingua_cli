import os
from datetime import datetime, timezone
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.exc import IntegrityError

load_dotenv()

Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URL', 'sqlite:///lingua.db'))
Session = sessionmaker(bind=engine)

# Join table for many-to-many between Lesson and Word
lesson_words = Table(
    'lesson_words',
    Base.metadata,
    Column('lesson_id', Integer, ForeignKey('lessons.id'), primary_key=True),
    Column('word_id', Integer, ForeignKey('words.id'), primary_key=True)
)

class Learner(Base):
    __tablename__ = 'learners'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    target_language = Column(String, nullable=False)
    proficiency_level = Column(String, default='Beginner')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    sessions = relationship('PracticeSession', back_populates='learner')
    
    total_learners = 0
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Learner.total_learners += 1
    
    def add_session(self, session, score, lesson_id=None, feedback=""):
        new_session = PracticeSession(learner_id=self.id, lesson_id=lesson_id, score=score, feedback=feedback)
        session.add(new_session)
        session.commit()
        self.update_level(session)
    
    def update_level(self, session):
        avg_score = self.get_average_score(session)
        if avg_score > 90:
            self.proficiency_level = 'Advanced'
        elif avg_score > 70:
            self.proficiency_level = 'Intermediate'
        else:
            self.proficiency_level = 'Beginner'
        session.commit()
    
    def get_average_score(self, session):
        total_sessions = len(self.sessions)
        if total_sessions == 0:
            return 0
        return sum(s.score for s in self.sessions) / total_sessions
    
    @property
    def fluency_score(self):
        if not self.sessions:
            return 0
        avg_score = sum(s.score for s in self.sessions) / len(self.sessions)
        return avg_score * (len(self.sessions) / 10)
    
    @classmethod
    def get_progress(cls, session, learner_id):
        learner = session.query(cls).get(learner_id)
        if not learner:
            return "Learner not found."
        total_sessions = len(learner.sessions)
        avg_score = learner.get_average_score(session)
        return f"Progress for {learner.name}: {total_sessions} sessions, average score: {avg_score:.2f}, fluency score: {learner.fluency_score:.2f}"
    
    def generate_quiz_prompt(self):
        return f"Create a quiz for {self.proficiency_level.lower()} {self.target_language} learner on vocabulary and grammar."  # Default for base class
    
    def __repr__(self):
        return f"<Learner(name={self.name}, language={self.target_language}, level={self.proficiency_level})>"

class BeginnerLearner(Learner):
    def generate_quiz_prompt(self):
        return f"Create a simple quiz for beginner {self.target_language} learner on basic vocabulary."

class AdvancedLearner(Learner):
    def generate_quiz_prompt(self):
        return f"Create an advanced quiz for {self.proficiency_level} {self.target_language} learner on conversation and grammar."

class Word(Base):
    __tablename__ = 'words'
    
    id = Column(Integer, primary_key=True)
    term = Column(String, nullable=False, unique=True)
    translation = Column(String, nullable=False)
    part_of_speech = Column(String)
    example_sentence = Column(String)
    
    lessons = relationship('Lesson', secondary=lesson_words, back_populates='words')
    
    def __repr__(self):
        return f"<Word(term={self.term}, translation={self.translation})>"

class Lesson(Base):
    __tablename__ = 'lessons'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    difficulty = Column(Integer, default=1)
    
    words = relationship('Word', secondary=lesson_words, back_populates='lessons')
    sessions = relationship('PracticeSession', back_populates='lesson')
    
    def __repr__(self):
        return f"<Lesson(title={self.title}, difficulty={self.difficulty})>"

class PracticeSession(Base):
    __tablename__ = 'practice_sessions'
    
    id = Column(Integer, primary_key=True)
    learner_id = Column(Integer, ForeignKey('learners.id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    session_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    score = Column(Integer, default=0)
    feedback = Column(String)
    
    learner = relationship('Learner', back_populates='sessions')
    lesson = relationship('Lesson', back_populates='sessions')
    
    def __repr__(self):
        return f"<PracticeSession(learner_id={self.learner_id}, date={self.session_date}, score={self.score})>"