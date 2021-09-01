import datetime
from typing import List

import config
import telegram
from domain.model import Birthday
from service_layer.unit_of_work import AbstractUnitOfWork
from telegram import Update
from telegram.chatmember import ChatMember
from telegram.ext.callbackcontext import CallbackContext


def set_offset_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    if update.effective_message is None:
        return

    if update.effective_message is None:
        return

    user_id: int = update.effective_message.from_user.id
    chat_id: int = update.effective_message.chat.id

    with uow:
        # Check if it's admin, owner or staff
        # First check if it's a group
        if update.effective_chat.id < 0:
            staff_id_list: List[int] = [
                staff.user_id for staff in uow.repo.get_staff_list()
            ]
            chat_member: ChatMember

            try:
                chat_member = update.effective_chat.get_member(user_id=user_id)
            except telegram.error.TelegramError:
                return

            if not (
                chat_member.status in ["administrator", "creator"]
                or user_id in staff_id_list
            ):
                return

        # Get the offset from the args
        if len(context.args) != 1:
            text = "Número incorrecto de argumentos"
            update.effective_message.reply_text(text=text)
            return

        # Check argument is valid integer
        try:
            int(context.args[0])
        except ValueError:
            text = "El argumento debe ser un número entero"
            update.effective_message.reply_text(text=text)
            return

        offset: int = int(context.args[0])

        # Check that offset is in range
        if not (-23 <= offset <= 23):
            text = "El offset debe estar entre -23 y 23"
            update.effective_message.reply_text(text=text)
            return

        uow.repo.set_offset(chat_id=chat_id, offset=offset)

        current_hour = datetime.datetime.now().hour + offset

        if current_hour < 0:
            current_hour += 24
        elif current_hour >= 24:
            current_hour -= 24

        text = f"Offset configurado en {offset}.\nHora actual: {current_hour}"
        update.effective_message.reply_text(text=text)

        uow.commit()
