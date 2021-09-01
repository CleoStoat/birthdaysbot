from helpers.command_helpers import CommandData

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

COMMANDS = [
    CommandData(
        callback=add_hour_cmd,
        name="",
        description="",
    ),
    CommandData(
        callback=del_hour_cmd,
        name="",
        description="",
    ),
    CommandData(
        callback=add_staff_cmd,
        name="",
        description="",
    ),
    CommandData(
        callback=get_all_cmd,
        name="",
        description="",
    ),
    CommandData(
        callback=initialize_cmd,
        name="",
        description="",
    ),
    CommandData(
        callback=set_bd_cmd,
        name="",
        description="",
    ),
    CommandData(
        callback=set_bd_manual_cmd,
        name="",
        description="",
    ),
    CommandData(
        callback=set_offset_cmd,
        name="",
        description="",
    ),
    CommandData(
        callback=show_bd_cmd,
        name="",
        description="",
    ),
    CommandData(
        callback=show_hours_cmd,
        name="",
        description="",
    ),
    CommandData(
        callback=trigger_bd_message_check_cmd,
        name="",
        description="",
    ),
    CommandData(
        callback=set_congrats_message_cmd,
        name="",
        description="",
    ),
    CommandData(
        callback=show_cur_hour_cmd,
        name="",
        description="",
    ),
]
