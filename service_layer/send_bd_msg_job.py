import datetime
from service_layer.get_chat_member_cached import get_chat_member

from domain.model import Birthday
from typing import List, Optional

from telegram.chatmember import ChatMember
from telegram.ext.callbackcontext import CallbackContext

from service_layer.unit_of_work import AbstractUnitOfWork


def send_bd_msg(context: CallbackContext, uow: AbstractUnitOfWork, chat_id: Optional[int] = None) -> None:
    with uow:

        current_hour = datetime.datetime.now().hour

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        tomorrow = today + datetime.timedelta(days=1)

        birthdays_yesterday = uow.repo.get_bd_list_at_date(
            curr_day=yesterday.day, curr_month=yesterday.month
        )
        birthdays_today = uow.repo.get_bd_list_at_date(
            curr_day=today.day, curr_month=today.month
        )
        birthdays_tomorrow = uow.repo.get_bd_list_at_date(
            curr_day=tomorrow.day, curr_month=tomorrow.month
        )

        group_confs = uow.repo.get_all_group_config()

        if chat_id is not None:
            group_confs = [uow.repo.get_group_config(chat_id=chat_id)]
            
        for gc in group_confs:
            group_tz_offset = int(gc.offset)

            group_current_hour: int
            birthdays: List[Birthday]

            hour_offset = current_hour + group_tz_offset
            if hour_offset < 0:
                group_current_hour = 24 + hour_offset
                birthdays = birthdays_yesterday
            elif hour_offset >= 24:
                group_current_hour = hour_offset - 24
                birthdays = birthdays_tomorrow
            else:
                group_current_hour = hour_offset
                birthdays = birthdays_today

            scheduled_hours = [group_hour.hour for group_hour in uow.repo.get_hours(gc.chat_id)]

            if group_current_hour not in scheduled_hours:
                continue

            for bd in birthdays:
                chat_member: Optional[ChatMember] = get_chat_member(
                    chat_id=gc.chat_id, 
                    user_id=bd.user_id,
                    bot=context.bot
                    )
                
                if chat_member is None:
                    continue
                
                if chat_member.status in ["kicked", "left"]:
                    continue

                text = uow.repo.get_congrats_message(chat_id=gc.chat_id)

                name = chat_member.user.name
                text = text.replace("_NAME", name)

                context.bot.send_message(chat_id=gc.chat_id, text=text)

        uow.commit()

