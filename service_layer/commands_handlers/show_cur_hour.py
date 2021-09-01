import datetime
from domain.model import Birthday
from typing import List, Tuple
from telegram import Update
import telegram
from telegram.chatmember import ChatMember
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def show_cur_hour_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    if update.effective_message is None:
        return

    chat_id: int = update.effective_message.chat_id
    
    if update.effective_message.from_user is None:
        return


    with uow:
        chat_id: int = update.effective_chat.id
        group_conf = uow.repo.get_group_config(chat_id=chat_id)

        current_hour = datetime.datetime.now().hour

        group_tz_offset = group_conf.offset
        group_current_hour: int

        hour_offset = current_hour + group_tz_offset
        if hour_offset < 0:
            group_current_hour = 24 + hour_offset
        elif hour_offset >= 24:
            group_current_hour = hour_offset - 24
        else:
            group_current_hour = hour_offset

        text = f"Hora actual: {current_hour}"
        update.effective_message.reply_text(text=text)

        uow.commit()
