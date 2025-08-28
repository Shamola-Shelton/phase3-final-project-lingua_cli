# LinguaCLI: AI-Powered CLI Language Learning Companion

## Project Overview
LinguaCLI is an interactive command-line interface (CLI) application designed to help self-learners practice and improve their skills in a target language (e.g., Spanish, French, Japanese). Leveraging Python, SQLAlchemy, OpenAI's Chat Completions API, and Click, it offers personalized vocabulary quizzes, grammar corrections, and conversational simulations. The app adapts to user proficiency levels using spaced repetition (via linked lists) and grammar rule organization (via binary trees), with progress tracking stored in a local SQLite database. Inspired by 2025 trends in AI-driven language learning (e.g., Duolingo, TalkPal), LinguaCLI is ideal for travelers, hobbyists, or anyone seeking flexible, offline-capable language practice.

This project fulfills Phase 3 requirements, demonstrating proficiency in:
- **Python Fundamentals**: Control flow, functions, error handling.
- **Object-Oriented Programming (OOP)**: Classes, properties, class methods.
- **SQL/ORM**: SQLite with SQLAlchemy, relationships, migrations via Alembic.
- **CLI Development**: Interactive menus with Click.
- **Data Structures and Algorithms (DSA)**: Linked lists, binary trees, searching/sorting.
- **API Integration**: OpenAI for dynamic content generation.
- **Testing**: Unit and integration tests with pytest, achieving 80% coverage.

## Features
- **User Authentication**: Create accounts and log in with username/password (passwords hidden during input).
- **Vocabulary Management**: Add words with translations, stored in SQLite.
- **AI-Powered Exercises**:
  - Vocabulary quizzes tailored to proficiency level (Beginner, Intermediate, Advanced).
  - Grammar correction with detailed feedback.
  - Conversational practice with AI responses and feedback.
- **Adaptive Learning**: Spaced repetition for weak words using a doubly linked list; grammar rules organized in a binary tree.
- **Progress Tracking**: View session history, average scores, and fluency metrics.
- **Flashcard Export**: Export learned words to CSV for offline review.
- **Interactive Menus**: Initial menu (login/new user) and main menu for features, with options to return or quit.

## Tech Stack
- **Python**: 3.12+ (type hints, performance).
- **Libraries**:
  - `sqlalchemy` (2.0+): ORM for database interactions.
  - `alembic` (1.13+): Database migrations.
  - `openai` (1.40+): Chat Completions API (model: gpt-4o).
  - `python-dotenv` (1.0+): Environment variable management.
  - `click` (8.1+): CLI interface.
  - `getpass`: Hidden password input.
  - `csv`: Built-in for flashcard export.
  - `pytest` (8.0+): Testing framework.
  - `ipdb` (0.13+): Debugging.
- **Database**: SQLite (`lingua.db`), lightweight and local.
- **Environment**: Virtualenv or pipenv for dependency isolation.

## Project Structure
```
lingua_cli/
├── venv/                   # Virtual environment
├── Pipfile                # Optional: pipenv dependencies
├── .env                   # Environment variables (OPENAI_API_KEY, DATABASE_URL)
├── .env.example           # Template for .env
├── .gitignore             # Ignores venv, lingua.db, .env, caches
├── alembic.ini            # Alembic configuration
├── README.md              # This file
├── blog.md                # Project reflections
├── app.py                 # Entry point: starts interactive menu
├── lib/
│   ├── __init__.py
│   ├── cli.py             # CLI logic (menus, commands)
│   ├── models.py          # SQLAlchemy models (Learner, Word, Lesson, PracticeSession)
│   ├── helpers.py         # AI integration, utility functions
│   ├── seed.py            # Database seeding script
│   ├── structures.py      # Custom data structures (linked list, tree)
│   └── db/
│       ├── migrations/    # Alembic migration files
│       └── __init__.py
└── tests/
    ├── test_models.py     # Tests for ORM and OOP
    ├── test_cli.py        # Tests for CLI commands
    ├── test_structures.py # Tests for data structures
    └── test_integration.py # End-to-end integration tests
```

## Setup Instructions
1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd lingua_cli
   ```

2. **Set Up Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```
   pip install sqlalchemy alembic python-dotenv click openai pytest ipdb
   ```

4. **Configure Environment**:
   - Copy `.env.example` to `.env`:
     ```
     cp .env.example .env
     ```
   - Edit `.env`:
     ```
     DATABASE_URL=sqlite:///lingua.db
     OPENAI_API_KEY=your_openai_key_here  # Optional for AI features
     ```
   - Obtain an OpenAI API key from [openai.com](https://openai.com) if using AI features; otherwise, fallback responses are used.

5. **Initialize Database**:
   - Initialize migrations (if not already done):
     ```
     alembic init lib/db/migrations
     ```
   - Edit `alembic.ini` to set `sqlalchemy.url = sqlite:///lingua.db`.
   - Update `lib/db/migrations/env.py` to include:
     ```python
     from lib.models import Base
     target_metadata = Base.metadata
     ```
   - Generate and apply migrations:
     ```
     alembic revision --autogenerate -m "Initial schema"
     alembic revision --autogenerate -m "Add password and unique name to learners"
     alembic upgrade head
     ```

6. **Seed Database**:
   ```
   python lib/seed.py
   ```
   - Creates sample users (Alice/alicepass, Bob/bobpass), words, lessons, and sessions.

## Usage
Run the app:
```
python app.py
```

### Initial Menu
```
Welcome to LinguaCLI!
1: Log in
2: New user
r: Return
q: Quit
Enter choice:
```
- **Log in (1)**: Enter username/password (e.g., `Alice`/`alicepass`).
- **New user (2)**: Create a new account with username, password, and target language.
- **Return (r)**: Refreshes initial menu.
- **Quit (q)**: Exits app.

### Main Menu (after login)
```
Main Menu:
1: Add Word
2: Vocab Quiz
3: Grammar Practice
4: Conversation
5: View Progress
6: Review Words
7: Export Flashcards
8: Logout
r: Return
Enter choice:
```
- **Add Word (1)**: Add vocabulary (e.g., `amigo`/`friend`).
- **Vocab Quiz (2)**: AI-generated or fallback quiz based on proficiency (e.g., "What is 'hola'?").
- **Grammar Practice (3)**: Correct sentences with AI feedback (e.g., "Hola como estas" → corrections).
- **Conversation (4)**: Interactive AI chat; type `quit` to exit.
- **View Progress (5)**: Show sessions, average score, fluency score.
- **Review Words (6)**: Spaced repetition for weak words (scores < 70).
- **Export Flashcards (7)**: Save words to `flashcards.csv`.
- **Logout (8)**: Return to initial menu.
- **Return (r)**: Return to initial menu.
- After each command, choose `q` to quit or `r` to return to main menu.

### Example Flow
```
$ python app.py
Welcome to LinguaCLI!
1: Log in
2: New user
r: Return
q: Quit
Enter choice: 1
Username: Alice
Password: alicepass
Logged in as Alice. Level: Intermediate
Main Menu:
1: Add Word
2: Vocab Quiz
...
Enter choice: 2
Question 1: What is 'hola' in English?
Your answer: hello
Correct!
...
Score: 3/3
q: Quit app
r: Return to main menu
Enter choice: r
Main Menu:
...
```

## Testing
Run automated tests (80% coverage):
```
pytest -v
```
- **Unit Tests**: `test_models.py` (ORM, OOP), `test_structures.py` (DSA), `test_cli.py` (commands).
- **Integration Tests**: `test_integration.py` (end-to-end flows with mocked AI).

### Manual Testing
1. **Log in**: Use `Alice`/`alicepass` or create new user.
2. **Vocab Quiz**: Answer questions; verify score updates in progress.
3. **Grammar/Conversation**: Test AI responses (requires `OPENAI_API_KEY`) or fallbacks.
4. **Progress/Export**: Check stats and CSV output.
5. **Edge Cases**:
   - Invalid login (`Alice`/`wrong`): "Invalid username or password."
   - Duplicate word/user: "Word already exists"/"Username taken."
   - No login: Try commands → "Log in first."

## Database Schema
- **Learner**: `id`, `name` (unique), `password`, `target_language`, `proficiency_level`, `created_at`.
- **Word**: `id`, `term` (unique), `translation`, `part_of_speech`, `example_sentence`.
- **Lesson**: `id`, `title`, `description`, `difficulty`.
- **PracticeSession**: `id`, `learner_id`, `lesson_id`, `session_date`, `score`, `feedback`.
- **Relationships**:
  - `Learner` ↔ `PracticeSession` (one-to-many).
  - `Lesson` ↔ `PracticeSession` (one-to-many).
  - `Lesson` ↔ `Word` (many-to-many via `lesson_words`).

## Data Structures
- **DoublyLinkedList**: Spaced repetition for weak words (move correct answers to end).
- **GrammarTree**: Binary tree for grammar rules, traversed in-order for practice.
- **Algorithms**: Bubble sort for word lists, binary search potential for sorted data.

## Challenges & Solutions
- **Session Management**: `DetachedInstanceError` fixed by storing `current_user_id` and re-querying learners.
- **AI Integration**: Handled API errors with static fallbacks; parsed responses with regex.
- **SQLite Constraints**: Used Alembic batch mode for unique constraint on `name`.
- **Quiz Display**: Ensured questions display before prompts with `sys.stdout.flush()`.

## Future Enhancements
- Hash passwords with `bcrypt`.
- Persist spaced repetition lists in DB.
- Add voice input/output with OpenAI Realtime API.
- Support more languages with dynamic fallbacks.
- Add GUI or web interface.

## License
MIT