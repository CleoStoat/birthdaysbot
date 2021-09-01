from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def add_staff_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    if update.effective_message is None:
        return

    if update.effective_message.from_user is None:
        return

    chat_id: int = update.effective_message.chat_id
    user_id: int = update.effective_message.from_user.id

    # Check if it user is owner
    if user_id != config.get_bot_owner_user_id():
        text = "Sólo el dueño del bot puede usar este comando"
        update.effective_message.reply_text(text=text)
        return

    # Check that message is a reply
    if update.effective_message.reply_to_message is None:
        text = "El mensaje debe ser una respuesta"
        update.effective_message.reply_text(text=text)
        return

    reply_user_id: int = update.effective_message.reply_to_message.from_user.id
    reply_user_name: str = update.effective_message.reply_to_message.from_user.full_name

    with uow:
        # Check if user is part of the staff
        if reply_user_id in [staff.user_id for staff in uow.repo.get_staff_list()]:
            text = "El usuario ya es parte del staff"
            update.effective_message.reply_text(text=text)
            return

        uow.repo.add_staff_member(user_id=user_id)
        text = f"Agregado a {reply_user_name} al staff"
        update.effective_message.reply_text(text=text)

        uow.commit()
