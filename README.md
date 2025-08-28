# README.md (New for Day 8)
# LinguaCLI: AI-Powered CLI Language Learning App

## Overview
LinguaCLI is a terminal-based app for learning languages with personalized AI exercises, progress tracking, and adaptive practice. Built with Python, SQLAlchemy, OpenAI, and Click.

## Setup
1. Clone the repo.
2. Create venv: `python -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install deps: `pip install sqlalchemy alembic python-dotenv pytest ipdb click openai`
5. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` and `DATABASE_URL=sqlite:///lingua.db`.
6. Init migrations: `alembic init lib/db/migrations` (if not done).
7. Generate migration: `alembic revision --autogenerate -m "Initial schema"`
8. Apply: `alembic upgrade head`
9. Seed DB: `python lib/seed.py`

## Usage
Run `python app.py --help` for commands.
- `create-user`: Create profile.
- `login`: Log in.
- `add-word`: Add vocabulary.
- `quiz-vocab`: AI-generated quiz.
- `practice-grammar`: Sentence correction.
- `simulate-convo`: Conversational practice.
- `review-words`: Spaced repetition.
- `view-progress`: Stats.
- `export-flashcards`: CSV export.
- `main`: Interactive menu.
- `logout`: Log out.

Example: `python app.py main` after login.

## Features
- OOP for learner personalization.
- SQLAlchemy ORM for DB (SQLite).
- Data structures for adaptive learning (linked lists, trees).
- OpenAI for dynamic content.
- Click CLI for UX.
- Pytest for testing.

## Testing
Run `pytest -v` for unit/integration tests (80% coverage).

## License
MIT