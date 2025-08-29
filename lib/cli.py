# lib/cli.py
import click
import getpass
import csv
import sys
from lib.models import Session, Learner, Word
from lib.helpers import generate_quiz, correct_grammar, simulate_convo, InvalidInputError, get_proficiency_levels

current_user_id = None  # Store ID instead of object to avoid detachment

@click.group()
def cli():
    pass

def initial_menu():
    while True:
        click.echo("\nWelcome to LinguaCLI!\n1: Log in\n2: New user\nr: Return\nq: Quit")
        choice = click.prompt("Enter choice")
        if choice == '1':
            log_in()
            if current_user_id:
                main_menu()
        elif choice == '2':
            new_user()
        elif choice.lower() == 'r':
            continue  # Return to same menu
        elif choice.lower() == 'q':
            break
        else:
            click.echo("Invalid choice.")

def log_in():
    global current_user_id
    name = click.prompt("Username")
    password = getpass.getpass("Password: ")
    session = Session()
    learner = session.query(Learner).filter_by(name=name, password=password).first()
    if learner:
        current_user_id = learner.id
        click.echo(f"Logged in as {name}. Level: {learner.proficiency_level}")
    else:
        click.echo("Invalid username or password.")
    session.close()

def new_user():
    name = click.prompt("Username")
    password = getpass.getpass("Password: ")
    language = click.prompt("Target language", default="Spanish")
    session = Session()
    if session.query(Learner).filter_by(name=name).first():
        click.echo("Username taken.")
        session.close()
        return
    learner = Learner(name=name, password=password, target_language=language)
    session.add(learner)
    try:
        session.commit()
        click.echo(f"User {name} created.")
    except IntegrityError:
        session.rollback()
        click.echo("Error creating user (possible duplicate).")
    session.close()

@cli.command(name='logout')
def logout():
    global current_user_id
    current_user_id = None
    click.echo("Logged out.")
    initial_menu()

def add_word():
    global current_user_id
    if not current_user_id:
        click.echo("Log in first.")
        return
    term = click.prompt("Term")
    if not term.isalpha():
        click.echo("Invalid term: Letters only (Unicode supported).")
        return
    translation = click.prompt("Translation")
    try:
        session = Session()
        word = Word(term=term, translation=translation)
        session.add(word)
        session.commit()
        click.echo(f"Added word: {term} -> {translation}")
    except IntegrityError:
        session.rollback()
        click.echo("Word already exists.")
    session.close()
    click.echo("\nq: Quit app\nr: Return to main menu")
    choice = click.prompt("Enter choice")
    if choice.lower() == 'q':
        sys.exit(0)

def view_progress():
    global current_user_id
    if not current_user_id:
        click.echo("Log in first.")
        return
    session = Session()
    learner = session.query(Learner).filter_by(id=current_user_id).first()
    if not learner:
        click.echo("User not found.")
        session.close()
        return
    progress = Learner.get_progress(session, learner.id)
    click.echo(progress)
    # Display proficiency criteria using tuples
    levels = get_proficiency_levels()
    click.echo("\nProficiency Level Criteria:")
    for level, min_score in levels:
        click.echo(f"{level}: Average score >= {min_score}")
    session.close()
    click.echo("\nq: Quit app\nr: Return to main menu")
    choice = click.prompt("Enter choice")
    if choice.lower() == 'q':
        sys.exit(0)

def export_flashcards():
    global current_user_id
    if not current_user_id:
        click.echo("Log in first.")
        return
    session = Session()
    learner = session.query(Learner).filter_by(id=current_user_id).first()
    if not learner:
        click.echo("User not found.")
        session.close()
        return
    words = set()
    for s in learner.sessions:
        if s.lesson:
            words.update(s.lesson.words)
    with open('flashcards.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['term', 'translation'])
        for word in words:
            writer.writerow([word.term, word.translation])
    click.echo("Exported to flashcards.csv")
    session.close()
    click.echo("\nq: Quit app\nr: Return to main menu")
    choice = click.prompt("Enter choice")
    if choice.lower() == 'q':
        sys.exit(0)

def review_words():
    global current_user_id
    if not current_user_id:
        click.echo("Log in first.")
        return
    session = Session()
    learner = session.query(Learner).filter_by(id=current_user_id).first()
    if not learner:
        click.echo("User not found.")
        session.close()
        return
    learner.load_weak_words(session)
    review_list = learner.review_weak_words()
    if review_list.head:
        current = review_list.head
        words = []
        while current:
            words.append(current.data)
            current = current.next
        click.echo(f"Review list: {', '.join(words)}")
    else:
        click.echo("No weak words.")
    session.close()
    click.echo("\nq: Quit app\nr: Return to main menu")
    choice = click.prompt("Enter choice")
    if choice.lower() == 'q':
        sys.exit(0)

def quiz_vocab():
    global current_user_id
    if not current_user_id:
        click.echo("Log in first.")
        return
    session = Session()
    learner = session.query(Learner).filter_by(id=current_user_id).first()
    if not learner:
        click.echo("User not found.")
        session.close()
        return
    questions = generate_quiz(learner)
    if not questions:
        click.echo("No quiz available. Try setting OPENAI_API_KEY.")
        session.close()
        return
    score = 0
    for i, (q, ans) in enumerate(questions, 1):
        click.echo(f"\nQuestion {i}: {q}", nl=True)
        sys.stdout.flush()
        user_ans = click.prompt("Your answer")
        if user_ans.strip().lower() == ans.strip().lower():
            score += 1
            click.echo("Correct!")
        else:
            click.echo(f"Wrong. Correct answer: {ans}")
    click.echo(f"\nScore: {score}/{len(questions)}")
    learner.add_session(session, score * (100 / len(questions)) if questions else 0)
    session.close()
    click.echo("\nq: Quit app\nr: Return to main menu")
    choice = click.prompt("Enter choice")
    if choice.lower() == 'q':
        sys.exit(0)

def practice_grammar():
    global current_user_id
    if not current_user_id:
        click.echo("Log in first.")
        return
    session = Session()
    learner = session.query(Learner).filter_by(id=current_user_id).first()
    if not learner:
        click.echo("User not found.")
        session.close()
        return
    sentence = click.prompt("Enter sentence")
    feedback = correct_grammar(sentence, learner.target_language)
    click.echo(feedback)
    session.close()
    click.echo("\nq: Quit app\nr: Return to main menu")
    choice = click.prompt("Enter choice")
    if choice.lower() == 'q':
        sys.exit(0)

def simulate_convo_cmd():
    global current_user_id
    if not current_user_id:
        click.echo("Log in first.")
        return
    session = Session()
    learner = session.query(Learner).filter_by(id=current_user_id).first()
    if not learner:
        click.echo("User not found.")
        session.close()
        return
    click.echo("Start conversation (type 'quit' to end).")
    while True:
        user_input = click.prompt("You")
        if user_input.lower() == 'quit':
            break
        response, feedback = simulate_convo(learner, user_input)
        click.echo(f"AI: {response}")
        click.echo(f"Feedback: {feedback}")
    session.close()
    click.echo("\nq: Quit app\nr: Return to main menu")
    choice = click.prompt("Enter choice")
    if choice.lower() == 'q':
        sys.exit(0)

def main_menu():
    global current_user_id
    if not current_user_id:
        click.echo("Log in first.")
        return
    while True:
        click.echo("\nMain Menu:\n1: Add Word\n2: Vocab Quiz\n3: Grammar Practice\n4: Conversation\n5: View Progress\n6: Review Words\n7: Export Flashcards\n8: Logout\nr: Return")
        choice = click.prompt("Enter choice")
        if choice == '1':
            add_word()
        elif choice == '2':
            quiz_vocab()
        elif choice == '3':
            practice_grammar()
        elif choice == '4':
            simulate_convo_cmd()
        elif choice == '5':
            view_progress()
        elif choice == '6':
            review_words()
        elif choice == '7':
            export_flashcards()
        elif choice == '8':
            logout()
            break
        elif choice.lower() == 'r':
            break  # Return to initial menu
        else:
            click.echo("Invalid choice.")