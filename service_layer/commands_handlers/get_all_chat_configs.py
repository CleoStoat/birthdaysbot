from telegram import Update
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork
import config


def get_all_cmd(
    update: Update, context: CallbackContext, uow: AbstractUnitOfWork
) -> None:
    if update.effective_message is None:
        return

    configs = None
    with uow:
        configs = uow.repo.get_all_configs()
        print(configs)
        update.effective_message.reply_text("Test")
        uow.commit()
