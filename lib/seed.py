# lib/seed.py
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.models import Session, Learner, Word, Lesson, PracticeSession, lesson_words
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import delete
from datetime import datetime, timezone

def seed_data():
    session = Session()
    
    try:
        # Clear existing data (for reseeding)
        session.execute(delete(lesson_words))  # Clear join table
        session.query(PracticeSession).delete()
        session.query(Learner).delete()
        session.query(Word).delete()
        session.query(Lesson).delete()
        session.commit()
    except:
        session.rollback()
        print("Error clearing tables; rolling back.")
        session.close()
        return
    
    try:
        # Sample Learners
        learner1 = Learner(name="Alice", target_language="Spanish", proficiency_level="Beginner")
        learner2 = Learner(name="Bob", target_language="French", proficiency_level="Intermediate")
        session.add_all([learner1, learner2])
        session.commit()
        
        # Sample Words (Spanish examples)
        words = [
            Word(term="hola", translation="hello", part_of_speech="interjection", example_sentence="Hola, ¿cómo estás?"),
            Word(term="adios", translation="goodbye", part_of_speech="interjection", example_sentence="Adiós, hasta luego."),
            Word(term="gracias", translation="thank you", part_of_speech="interjection")
        ]
        for word in words:
            if not session.query(Word).filter_by(term=word.term).first():
                session.add(word)
        session.commit()
        
        # Sample Lesson
        lesson1 = Lesson(title="Basic Greetings", description="Learn simple hello and goodbye phrases.", difficulty=1)
        session.add(lesson1)
        session.commit()
        
        # Assign words to lesson (many-to-many)
        lesson1.words = words
        session.commit()
        
        # Sample Practice Session
        session1 = PracticeSession(learner_id=learner1.id, lesson_id=lesson1.id, score=85, feedback="Good start!")
        session.add(session1)
        session.commit()
        
        # Test OOP methods
        learner1.add_session(session, score=95)  # Add another session, update level
        print(f"Total learners: {Learner.total_learners}")
        print(f"Fluency score for Alice: {learner1.fluency_score:.2f}")
        print(learner1.generate_quiz_prompt())  # Beginner prompt
        
        print("Database seeded successfully!")
    except IntegrityError as e:
        session.rollback()
        print(f"Error seeding data: {e}")
    except Exception as e:
        session.rollback()
        print(f"Unexpected error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_data()