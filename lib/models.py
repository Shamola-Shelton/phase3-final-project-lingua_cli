# lib/models.py
import os
from datetime import datetime
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
    proficiency_level = Column(String, default='Beginner')  # e.g., Beginner, Intermediate, Advanced
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sessions = relationship('PracticeSession', back_populates='learner')
    
    # Class method for progress tracking (example)
    @classmethod
    def get_progress(cls, session, learner_id):
        learner = session.query(cls).get(learner_id)
        if not learner:
            return "Learner not found."
        total_sessions = len(learner.sessions)
        avg_score = sum(s.score for s in learner.sessions) / total_sessions if total_sessions > 0 else 0
        return f"Progress for {learner.name}: {total_sessions} sessions, average score: {avg_score:.2f}"
    
    def __repr__(self):
        return f"<Learner(name={self.name}, language={self.target_language}, level={self.proficiency_level})>"

class Word(Base):
    __tablename__ = 'words'
    
    id = Column(Integer, primary_key=True)
    term = Column(String, nullable=False, unique=True)  # e.g., "hola"
    translation = Column(String, nullable=False)  # e.g., "hello"
    part_of_speech = Column(String)  # e.g., "noun"
    example_sentence = Column(String)
    
    # Relationships
    lessons = relationship('Lesson', secondary=lesson_words, back_populates='words')
    
    def __repr__(self):
        return f"<Word(term={self.term}, translation={self.translation})>"

class Lesson(Base):
    __tablename__ = 'lessons'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # e.g., "Basic Greetings"
    description = Column(String)
    difficulty = Column(Integer, default=1)  # 1-5 scale
    
    # Relationships
    words = relationship('Word', secondary=lesson_words, back_populates='lessons')
    sessions = relationship('PracticeSession', back_populates='lesson')
    
    def __repr__(self):
        return f"<Lesson(title={self.title}, difficulty={self.difficulty})>"

class PracticeSession(Base):
    __tablename__ = 'practice_sessions'
    
    id = Column(Integer, primary_key=True)
    learner_id = Column(Integer, ForeignKey('learners.id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    session_date = Column(DateTime, default=datetime.utcnow)
    score = Column(Integer, default=0)  # e.g., out of 100
    feedback = Column(String)  # AI-generated later
    
    # Relationships
    learner = relationship('Learner', back_populates='sessions')
    lesson = relationship('Lesson', back_populates='sessions')
    
    def __repr__(self):
        return f"<PracticeSession(learner_id={self.learner_id}, date={self.session_date}, score={self.score})>"