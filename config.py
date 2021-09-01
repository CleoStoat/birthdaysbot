import os
from dotenv import load_dotenv

load_dotenv()

def get_sqlite_uri() -> str:

    dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.getenv("SQLITE_DB_PATH")
    sqlite_db_path = os.path.join(dir + os.sep, filename)
    return f"sqlite:///{sqlite_db_path}"


def get_bot_token() -> str:
    token = os.getenv("BOT_TOKEN")

    if token is None:
        raise Exception("Couldn't find BOT_TOKEN env variable")
    else:
        return token


def get_default_offset() -> int:
    return 0

def get_default_congrats_message() -> str:
    return "Happy birthday, _NAME."

def get_bot_owner_user_id() -> int:
    return int(os.getenv("BOT_OWNER_USER_ID", "0"))