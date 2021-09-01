from functools import cache, partial, wraps
from typing import DefaultDict, Optional
from telegram.chatmember import ChatMember
import telegram.error
from telegram.bot import Bot


_chats = {}

def get_chat_member(chat_id: int, user_id: int, bot: Bot) -> Optional[ChatMember]:
    if chat_id not in _chats:
        _chats[chat_id] = cache(
            partial(
                _query_chat_member, 
                chat_id=chat_id,
            )
        )

    return _chats[chat_id](user_id=user_id, bot=bot)


def _query_chat_member(chat_id: int, user_id: int, bot: Bot) -> Optional[ChatMember]:
    
    try:
        chat_member = bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return chat_member
    except telegram.error.TelegramError:
        return None

def clear_chat_member_cache(chat_id: int):
    if not _chats[chat_id]:
        return

    _chats[chat_id].cache_clear()

