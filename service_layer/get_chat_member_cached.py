from functools import lru_cache
from typing import Optional
from telegram.chatmember import ChatMember
import telegram.error
from telegram.bot import Bot


@lru_cache(maxsize=None)
def get_chat_member(chat_id: int, user_id: int, bot: Bot) -> Optional[ChatMember]:
    
    try:
        chat_member = bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return chat_member
    except telegram.error.TelegramError:
        return None