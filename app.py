# app.py (temporary for testing)
from lib.models import Session, Learner

if __name__ == "__main__":
    session = Session()
    
    # Create: Already done in seed
    
    # Read: Query all learners
    learners = session.query(Learner).all()
    for learner in learners:
        print(learner)
    
    # Update: Change a learner's level
    learner = session.query(Learner).filter_by(name="Alice").first()
    if learner:
        learner.proficiency_level = "Intermediate"
        session.commit()
        print(f"Updated: {learner}")
    
    # Delete: Remove a learner (careful, cascades to sessions)
    # learner_to_delete = session.query(Learner).filter_by(name="Bob").first()
    # if learner_to_delete:
    #     session.delete(learner_to_delete)
    #     session.commit()
    #     print("Deleted Bob.")
    
    # Test class method
    print(Learner.get_progress(session, 1))  # Assuming Alice's ID is 1
    
    session.close()