import datetime
import logging
from functools import partial

from telegram.ext import Updater
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.dispatcher import Dispatcher

import config
from adapters.orm import create_tables, start_mappers
from service_layer.commands_handlers.add_hour import add_hour_cmd
from service_layer.commands_handlers.del_hour import del_hour_cmd
from service_layer.commands_handlers.add_staff import add_staff_cmd
from service_layer.commands_handlers.get_all_chat_configs import get_all_cmd
from service_layer.commands_handlers.initialize import initialize_cmd
from service_layer.commands_handlers.set_bd import set_bd_cmd
from service_layer.commands_handlers.set_bd_manual import set_bd_manual_cmd
from service_layer.commands_handlers.set_offset import set_offset_cmd
from service_layer.commands_handlers.show_bd import show_bd_cmd
from service_layer.commands_handlers.show_hours import show_hours_cmd
from service_layer.commands_handlers.trigger_bd_message_check import trigger_bd_message_check_cmd
from service_layer.commands_handlers.set_congrats_msg import set_congrats_message_cmd
from service_layer.commands_handlers.show_cur_hour import show_cur_hour_cmd
from service_layer.send_bd_msg_job import send_bd_msg
from service_layer.unit_of_work import SqlAlchemyUnitOfWork


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    updater = construct_bot()
    updater.start_polling()
    updater.idle()


def construct_bot() -> Updater:
    start_mappers()
    create_tables()

    updater = Updater(token=config.get_bot_token())
    dispatcher: Dispatcher = updater.dispatcher

    # Instantiate SqlAlchemy Unit of Work
    uow = SqlAlchemyUnitOfWork()

    dispatcher.add_handler(CommandHandler("init", partial(initialize_cmd, uow=uow)))
    dispatcher.add_handler(CommandHandler("show_bd", partial(show_bd_cmd, uow=uow)))
    dispatcher.add_handler(CommandHandler("set_bd", partial(set_bd_cmd, uow=uow)))
    dispatcher.add_handler(CommandHandler("set_bd_manual", partial(set_bd_manual_cmd, uow=uow)))
    dispatcher.add_handler(CommandHandler("add_staff", partial(add_staff_cmd, uow=uow)))
    dispatcher.add_handler(CommandHandler("add_hour", partial(add_hour_cmd, uow=uow)))
    dispatcher.add_handler(CommandHandler("del_hour", partial(del_hour_cmd, uow=uow)))
    dispatcher.add_handler(CommandHandler("set_offset", partial(set_offset_cmd, uow=uow)))
    dispatcher.add_handler(CommandHandler("show_hours", partial(show_hours_cmd, uow=uow)))
    dispatcher.add_handler(CommandHandler("trigger_bd_message_check", partial(trigger_bd_message_check_cmd, uow=uow)))
    dispatcher.add_handler(CommandHandler("set_congrats_message", partial(set_congrats_message_cmd, uow=uow)))
    dispatcher.add_handler(CommandHandler("show_cur_hour", partial(show_cur_hour_cmd, uow=uow)))


    j = updater.job_queue

    interval = datetime.timedelta(hours=1)
    first = datetime.datetime(year=1900, month=1, day=1, hour=0, minute=0, second=0)
    job_func = partial(send_bd_msg, uow=uow)
    j.run_repeating(
        job_func, interval=interval, first=first, name="Send birthday message"
    )

    return updater


if __name__ == "__main__":
    main()
