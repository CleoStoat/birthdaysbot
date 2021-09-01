from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def initialize_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    if update.effective_message is None:
        return

    chat_id: int = update.effective_message.chat_id
    
    if update.effective_message.from_user is None:
        return


    with uow:
        # Check if it has been initialized already
        if uow.repo.get_group_config(chat_id=chat_id) is not None:
            # Chat has already been initialized
            text = "El bot ya había sido iniciado"
            update.effective_message.reply_text(text=text)
        else:
            # Add chat_config
            uow.repo.add_group_config(chat_id=chat_id)
            text = "El bot de cumpleaños inició exitosamente"
            update.effective_message.reply_text(text=text)

        uow.commit()
