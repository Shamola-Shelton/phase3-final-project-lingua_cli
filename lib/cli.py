# lib/cli.py
import click
from lib.models import Session, Learner, Word
from lib.helpers import generate_quiz, correct_grammar, simulate_convo

@click.group()
def cli():
    pass

@cli.command(name='create-user')
@click.option('--name', prompt='Name', help='Learner name.')
@click.option('--language', prompt='Target language', help='e.g., Spanish.')
def create_user(name, language):
    session = Session()
    learner = Learner(name=name, target_language=language)
    session.add(learner)
    session.commit()
    click.echo(f"Created user: {learner.name} ({learner.target_language})")

@cli.command(name='login')
@click.option('--name', prompt='Name', help='Learner name to log in.')
def login(name):
    session = Session()
    learner = session.query(Learner).filter_by(name=name).first()
    if learner:
        click.echo(f"Logged in as {learner.name}. Level: {learner.proficiency_level}")
        # Simulate "current user" – in full app, store in global or file
    else:
        click.echo("User not found.")

@cli.command(name='add-word')
@click.option('--term', prompt='Term', help='Word term.')
@click.option('--translation', prompt='Translation', help='Word translation.')
def add_word(term, translation):
    session = Session()
    word = Word(term=term, translation=translation)
    session.add(word)
    session.commit()
    click.echo(f"Added word: {term} -> {translation}")

@cli.command(name='view-progress')
@click.option('--learner_id', prompt='Learner ID', type=int, help='ID to view progress.')
def view_progress(learner_id):
    session = Session()
    progress = Learner.get_progress(session, learner_id)
    click.echo(progress)
# ... (keep existing imports and commands)

@cli.command(name='review-words')
@click.option('--learner_id', prompt='Learner ID', type=int, help='ID for review.')
def review_words(learner_id):
    session = Session()
    learner = session.query(Learner).get(learner_id)
    if learner:
        # Example usage
        learner.add_weak_word("hola")  # Simulate weak word
        review_list = learner.review_weak_words()
        click.echo(f"Review list: {review_list.head.data if review_list.head else 'No words'}")
    else:
        click.echo("Learner not found.")

@cli.command(name='quiz-vocab')
@click.option('--learner_id', prompt='Learner ID', type=int, help='ID for personalized quiz.')
def quiz_vocab(learner_id):
    session = Session()
    learner = session.query(Learner).get(learner_id)
    if learner:
        quiz = generate_quiz(learner)
        click.echo(f"Quiz: {quiz}")
    else:
        click.echo("Learner not found.")

@cli.command(name='practice-grammar')
@click.option('--sentence', prompt='Enter sentence', help='Sentence to correct.')
@click.option('--language', prompt='Language', help='e.g., Spanish.')
def practice_grammar(sentence, language):
    correction = correct_grammar(sentence, language)
    click.echo(f"Correction: {correction}")

@cli.command(name='simulate-convo')
@click.option('--language', prompt='Language', help='e.g., Spanish.')
def simulate_convo_cmd(language):
    history = []
    while True:
        user_input = click.prompt("You")
        if user_input.lower() == 'exit':
            break
        ai_response = simulate_convo(language, user_input, history)
        click.echo(f"AI: {ai_response}")
        history.extend([{"role": "user", "content": user_input}, {"role": "assistant", "content": ai_response}])

if __name__ == '__main__':
    cli()