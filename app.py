# app.py
from lib.models import Session, Learner, BeginnerLearner

if __name__ == "__main__":
    session = Session()
    
    # Read learners
    learners = session.query(Learner).all()
    for learner in learners:
        print(learner)
    
    # Use OOP: Add session and update level
    alice = session.query(Learner).filter_by(name="Alice").first()
    if alice:
        alice.add_session(session, score=95, lesson_id=1, feedback="Excellent!")
        print(f"Updated level: {alice.proficiency_level}")
        print(f"Fluency score: {alice.fluency_score:.2f}")
    
    # Class method
    print(Learner.get_progress(session, 1))
    
    # Inheritance example
    beginner = BeginnerLearner(name="Charlie", target_language="Spanish")
    session.add(beginner)
    session.commit()
    print(beginner.generate_quiz_prompt())
    
    session.close()