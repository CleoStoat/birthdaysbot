import datetime
from functools import lru_cache, partial
from service_layer.get_chat_member_cached import get_chat_member

from telegram.bot import Bot

from domain.model import Birthday
from typing import List, Optional, Tuple
from telegram import Update
import telegram
from telegram.chatmember import ChatMember
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config

def show_bd_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    if update.effective_message is None:
        return

    chat_id: int = update.effective_message.chat_id
    
    if update.effective_message.from_user is None:
        return


    with uow:
        # Get list of all birthdays
        birthdays = uow.repo.get_bd_list()


        # Find out which birthdays are members of this chat
        birthday_chat_members: List[Tuple[Birthday, ChatMember]] = []

        for bd in birthdays:
            update.effective_chat.send_action("typing")
            chat_member: Optional[ChatMember] = get_chat_member(
                chat_id=chat_id, 
                user_id=bd.user_id,
                bot=context.bot
                )
            
            if chat_member is None:
                continue
            
            if not chat_member.status not in ["kicked", "left"]:
                continue

            birthday_chat_members.append( (bd, chat_member) )


        text = "Cumpleaños del grupo:\n"
        for bd_chat_mem in birthday_chat_members:
            text += f"{bd_chat_mem[1].user.full_name}: {bd_chat_mem[0].day}/{bd_chat_mem[0].month}\n"

        update.effective_message.reply_text(text=text)

        uow.commit()
