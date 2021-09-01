import datetime
from typing import List

from domain.model import Birthday
from service_layer.unit_of_work import AbstractUnitOfWork
from telegram import Update
from telegram.chatmember import ChatMember
from telegram.ext.callbackcontext import CallbackContext
import telegram

from service_layer.send_bd_msg_job import send_bd_msg

def trigger_bd_message_check_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    chat_id: int = update.effective_chat.id
    send_bd_msg(context=context, uow=uow, chat_id=chat_id)
