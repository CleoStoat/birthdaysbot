import datetime
from typing import List

import config
import telegram
from domain.model import Birthday
from service_layer.unit_of_work import AbstractUnitOfWork
from telegram import Update
from telegram.chatmember import ChatMember
from telegram.ext.callbackcontext import CallbackContext


def show_hours_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    if update.effective_message is None:
        return

    if update.effective_message is None:
        return

    user_id: int = update.effective_message.from_user.id
    chat_id: int = update.effective_message.chat.id

    with uow:
        chat_hours = [group_hour.hour for group_hour in uow.repo.get_hours(chat_id=chat_id)]

        text = f"Itinerario de mensajes de cumpleaños:\n{str(sorted(chat_hours))[1:-1]}"
        update.effective_message.reply_text(text=text)

        uow.commit()
