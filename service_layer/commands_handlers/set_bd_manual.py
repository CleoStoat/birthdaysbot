import re
from typing import List
from telegram import Update
from telegram.chatmember import ChatMember
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def set_bd_manual_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    if update.effective_message is None:
        return

    if update.effective_message.from_user is None:
        return

    if update.effective_message.reply_to_message is None:
        return


    chat_id: int = update.effective_message.chat_id
    user_id: int = update.effective_message.from_user.id
    reply_user_id: int = update.effective_message.reply_to_message.from_user.id
    reply_user_name = update.effective_message.reply_to_message.from_user.full_name

    if not validate_command_format(command_args=context.args):
        text = "Por favor usa este comando con el siguiente formato: /set_bd_manual dia/mes\n\Ejemplo:\n/set_bd_manual 28/02"
        update.effective_message.reply_text(text=text)
        return
        
    day = int(context.args[0].split("/")[0])
    month = int(context.args[0].split("/")[1])

    with uow:
        # Check if user is part of the staff
        if user_id not in [staff.user_id for staff in uow.repo.get_staff_list()]:
            text = "Debes ser parte del staff para usar este comando"
            update.effective_message.reply_text(text=text)
            return


        # Find out if user already set the bd before
        if uow.repo.get_bd(user_id=reply_user_id):
            uow.repo.update_bd(user_id=reply_user_id, day=day, month=month)
            text = f"{reply_user_name} cumpleaños actualizado a {day}/{month}"
            update.effective_message.reply_text(text=text)
        else:
            uow.repo.add_bd(user_id=reply_user_id, day=day, month=month)
            text = f"{reply_user_name} cumpleaños configurado a {day}/{month}"
            update.effective_message.reply_text(text=text)
            
        uow.commit()


def validate_command_format(command_args: List[str]):
    if len(command_args) != 1:
        return False

    argument = command_args[0]

    if not re.match("^\d\d?/\d\d?$", argument):
        return False

    day_part, month_part = tuple(argument.split("/"))

    if not (1 <= int(month_part) <= 12):
        return False

    if not (1 <= int(day_part) <= 31):
        return False

    return True