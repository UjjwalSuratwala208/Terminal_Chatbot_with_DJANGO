# Django + ChatterBot Terminal Q&A Chatbot

This is a minimal terminal chatbot that uses **ChatterBot** for conversation and **Django** to manage the project structure.
You interact with the bot in your terminal (no web UI required).

## Quick Start

> **Tip:** Use Python **3.7 or above** for best compatibility with ChatterBot

```bash
# 1) Create & activate a virtual environment (Windows shown; use python3 on macOS/Linux)
python -m venv venv
venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Initialize Django (creates db.sqlite3)
python manage.py migrate

# 4) Run the terminal bot
python manage.py chat_app_terminal
```

Example:

```
You: Good morning! How are you doing?
Bot: I am doing very well, thank you for asking.
You: You're welcome.
Bot: Do you like hats?
```

Type `exit` or `quit` to leave the chat.

## Coding Standards & Comments

- **Docstrings & Inline comments** explain purpose and design choices in `chat_app_terminal.py`, `settings.py`, and `manage.py`.
- **Separation of concerns**: bot creation, training, and chat loop live in distinct helper methods.
- **Defensive error handling** keeps the REPL responsive even when exceptions occur.
- **Version-pinned dependencies** in `requirements.txt` improve install reliability.

## Project Structure

```
Terminal_Chatbot_With_DJANGO/
├─ manage.py
├─ requirements.txt
├─ manifest.json
├─ README.md
├─ chater_bot/
│  ├─ __init__.py
│  ├─ asgi.py
|  ├─ settings.py   
│  ├─ urls.py
│  └─ wsgi.py
└─ Chat_app/
   ├─ __init__.py
   ├─ apps.py
   └─ management/
      └─ commands/
         └─ chat_app_terminal.py
```

## Notes

- ChatterBot uses an SQLite database via SQLAlchemy. The first run may take longer as it trains on the `chatterbot_corpus` (English).
- If you face install issues, try a clean venv with Python 3.7 and above
- Replace the placeholder GitHub link in the report with your actual repository URL once you push this project.
