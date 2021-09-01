from bot_commands import COMMANDS
import datetime
from helpers.command_helpers import set_bot_commands
import logging
from functools import partial

from telegram.ext import Updater

import config
from adapters.orm import create_tables, start_mappers
from service_layer.send_bd_msg_job import send_bd_msg
from service_layer.unit_of_work import SqlAlchemyUnitOfWork


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    start_mappers()
    create_tables()

    updater = Updater(token=config.get_bot_token())

    # Instantiate SqlAlchemy Unit of Work
    uow = SqlAlchemyUnitOfWork()

    set_bot_commands(COMMANDS, updater, uow)

    j = updater.job_queue

    interval = datetime.timedelta(hours=1)
    first = datetime.datetime(year=1900, month=1, day=1, hour=0, minute=0, second=0)
    job_func = partial(send_bd_msg, uow=uow)
    j.run_repeating(
        job_func, interval=interval, first=first, name="Send birthday message"
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
