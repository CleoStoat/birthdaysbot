from typing import List
from telegram import Update
import telegram
from telegram.chatmember import ChatMember
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def set_congrats_message_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    with uow:
        if update.effective_message is None:
            return

        if update.effective_chat is None:
            return

        chat_id: int = update.effective_chat.id
        user_id: int = update.effective_user.id
            
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

        # Check if it has been initialized
        if uow.repo.get_group_config(chat_id=chat_id) is None:
            text = "Por favor inicializa el bot con /init antes de usar este comando"
            update.effective_message.reply_text(text=text)
            return

        # Check that message is a reply
        if update.effective_message.reply_to_message is None:
            text = "Usa este comando respondiendo a otro mensaje"
            update.effective_message.reply_text(text=text)
            return

        # Check replied message is text
        if update.effective_message.reply_to_message.text in [None, ""]:
            text = "El mensaje respondido debe ser un mensaje de texto"
            update.effective_message.reply_text(text=text)
            return

        congrats_message = update.effective_message.reply_to_message.text
        uow.repo.set_congrats_message(chat_id=chat_id, congrats_message=congrats_message)

        text = f"Mensaje de cumpleaños configurado en:\n\n{congrats_message}"
        update.effective_message.reply_text(text=text)

        uow.commit()
