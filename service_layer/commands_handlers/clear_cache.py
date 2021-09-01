from domain.model import Birthday
from typing import List
from telegram import Update
import telegram
from telegram.chatmember import ChatMember
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
from service_layer.get_chat_member_cached import clear_chat_member_cache
import config


def clear_cache_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    if update.effective_message is None:
        return

    user_id: int = update.effective_message.from_user.id

    with uow:
        # Check if it's admin, owner or staff
        staff_id_list: List[int] = [staff.user_id for staff in uow.repo.get_staff_list()]
        chat_member: ChatMember

        try:
            chat_member = update.effective_chat.get_member(user_id=user_id)
        except telegram.error.TelegramError:
            return

        if not (chat_member.status in ["administrator", "creator"] or user_id in staff_id_list):
            return

        uow.commit()
    
    clear_chat_member_cache()
    update.effective_message.reply_text("Cache cleared.")
