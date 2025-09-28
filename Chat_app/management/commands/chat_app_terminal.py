"""Terminal chatbot management command using ChatterBot.

Key ideas:
- We keep the UX in the terminal to focus on the core conversation loop.
- ChatterBot persists learned statements in a local SQLite DB (via SQLAlchemy).
- On the first run, we bootstrap knowledge using the English corpus.
- The command is idempotent; repeated runs reuse the same trained DB.

Run:
    python manage.py chat_app_terminal
Options:
    --read-only    Run without writing new statements to storage.
"""
from django.core.management.base import BaseCommand

# ChatterBot core and trainer
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

class Command(BaseCommand):
    """Django management command: launches an interactive chat loop."""
    help = "Run a terminal Q&A chatbot using ChatterBot. Type 'exit' or 'quit' to leave."

    def add_arguments(self, parser):
        # Useful when you want deterministic behavior for demos/tests.
        parser.add_argument(
            '--read-only',
            action='store_true',
            help='Run in read-only mode (no new statements written to storage).'
        )

    def _build_chatbot(self, read_only=False):
        """Construct and (if needed) train the ChatBot instance.

        The SQLStorageAdapter stores learned statements in `chatterbot.sqlite3`.
        We set a default response and similarity threshold to improve UX when the
        bot cannot find a good match.
        """
        chatbot = ChatBot(
            'TerminalBot',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri='sqlite:///chatterbot.sqlite3',  # Local file next to project
            logic_adapters=[
                {
                    # BestMatch selects the response with highest confidence.
                    'import_path': 'chatterbot.logic.BestMatch',
                    'default_response': "I'm not sure I understand. Can you rephrase?",
                    'maximum_similarity_threshold': 0.80
                }
            ],
            preprocessors=[
                # Normalize whitespace to improve matching quality.
                'chatterbot.preprocessors.clean_whitespace'
            ],
            read_only=read_only
        )
        return chatbot

    def _train_if_needed(self, chatbot):
        """Train using the built-in English corpus.

        Training is safe to call every run; ChatterBot caches statements in the
        SQLite DB. The first run can take longer as it builds the knowledge base.
        """
        self.stdout.write(self.style.NOTICE(
            'Preparing and training the bot (first run may take a while)...'
        ))
        trainer = ChatterBotCorpusTrainer(chatbot)
        try:
            trainer.train('chatterbot.corpus.english')
        except Exception as exc:
            # Handle environments lacking optional dependencies gracefully.
            self.stdout.write(self.style.WARNING(f'Training warning: {exc}'))
            self.stdout.write(self.style.WARNING(
                'Continuing; the bot may have limited knowledge this run.'
            ))

    def _chat_loop(self, chatbot):
        """Simple REPL (read-eval-print loop) for the terminal UX."""
        self.stdout.write(self.style.SUCCESS(
            'Bot is ready. Type your message, or type "exit" to quit.'
        ))
        while True:
            try:
                user_text = input('You: ').strip()
            except (EOFError, KeyboardInterrupt):
                # Allow Ctrl+D / Ctrl+C to exit cleanly.
                print()  # newline for nice terminal formatting
                break

            if user_text.lower() in {'exit', 'quit'}:
                print('Bot: Goodbye!')
                break

            if not user_text:
                # Ignore blank lines (helps when pasting multi-line content).
                continue

            try:
                response = chatbot.get_response(user_text)
                print(f'Bot: {response}')
            except Exception as exc:
                # Never crash the loop; report and keep going.
                print(f'Bot: Sorry, I ran into a problem: {exc}')

    def handle(self, *args, **options):
        """Entry point for `python manage.py runbot`.

        We separate construction/training/chatting into helpers to make the
        code easier to test and maintain.
        """
        chatbot = self._build_chatbot(read_only=options.get('read_only', False))
        self._train_if_needed(chatbot)
        self._chat_loop(chatbot)
