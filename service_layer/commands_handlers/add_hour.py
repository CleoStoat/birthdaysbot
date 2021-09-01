from domain.model import Birthday
from typing import List
from telegram import Update
import telegram
from telegram.chatmember import ChatMember
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def add_hour_cmd(
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
        staff_id_list: List[int] = [staff.user_id for staff in uow.repo.get_staff_list()]
        chat_member: ChatMember

        try:
            chat_member = update.effective_chat.get_member(user_id=user_id)
        except telegram.error.TelegramError:
            return

        if not (chat_member.status in ["administrator", "creator"] or user_id in staff_id_list):
            return

        # Get the hour from the args
        if len(context.args) != 1:
            text = "Numero incorreco de argumentos"
            update.effective_message.reply_text(text=text)
            return

        # Check argument is number
        if not context.args[0].isdigit():
            text = "Los argumentos deben ser numeros enteros"
            update.effective_message.reply_text(text=text)
            return

        hour: int = int(context.args[0])
        
        # Check that number is between 0 and 23 inclusive
        if not (0 <= hour <= 23):
            text = "La hora tiene que estar entre 0 y 23 (inclusivo)"
            update.effective_message.reply_text(text=text)
            return

        # Check if the hour doesn't exist already
        hours: List[int] = [gp_hour.hour for gp_hour in uow.repo.get_hours(chat_id=chat_id)]
        if hour in hours:
            text = f"La hora {hour} ya existe en el itinerario"
            update.effective_message.reply_text(text=text)
            return
            
        uow.repo.add_hour(chat_id=chat_id, hour=hour)
        text = f"Se configuró la hora {hour} exitosamente en el itinerario"
        update.effective_message.reply_text(text=text)

        uow.commit()
