from dotenv import load_dotenv
import os



dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if dotenv_path:
    load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
PHONE_NUMBERS = [i for i in os.getenv("PHONE_NUMBERS").split(",")]


if not BOT_TOKEN:
    raise ValueError("Bot Token is required.")