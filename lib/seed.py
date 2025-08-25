# lib/seed.py
from sqlalchemy.exc import IntegrityError
from lib.models import Session, Learner, Word, Lesson, PracticeSession
from datetime import datetime

def seed_data():
    session = Session()
    
    try:
        # Clear existing data (for reseeding)
        session.query(PracticeSession).delete()
        session.query(Learner).delete()
        session.query(Word).delete()
        session.query(Lesson).delete()
        session.commit()
    except:
        session.rollback()
    
    # Sample Learners
    learner1 = Learner(name="Alice", target_language="Spanish", proficiency_level="Beginner")
    learner2 = Learner(name="Bob", target_language="French", proficiency_level="Intermediate")
    session.add_all([learner1, learner2])
    session.commit()
    
    # Sample Words (Spanish examples)
    word1 = Word(term="hola", translation="hello", part_of_speech="interjection", example_sentence="Hola, ¿cómo estás?")
    word2 = Word(term="adios", translation="goodbye", part_of_speech="interjection", example_sentence="Adiós, hasta luego.")
    word3 = Word(term="gracias", translation="thank you", part_of_speech="interjection")
    session.add_all([word1, word2, word3])
    session.commit()
    
    # Sample Lesson
    lesson1 = Lesson(title="Basic Greetings", description="Learn simple hello and goodbye phrases.", difficulty=1)
    lesson1.words = [word1, word2, word3]  # Many-to-many association
    session.add(lesson1)
    session.commit()
    
    # Sample Practice Session
    session1 = PracticeSession(learner_id=learner1.id, lesson_id=lesson1.id, score=85, feedback="Good start!")
    session.add(session1)
    session.commit()
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()