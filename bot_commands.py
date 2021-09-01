from helpers.command_helpers import CommandData

from service_layer.commands_handlers.add_hour import add_hour_cmd
from service_layer.commands_handlers.del_hour import del_hour_cmd
from service_layer.commands_handlers.add_staff import add_staff_cmd
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
        name="add_hour",
        description="(admin) Agrega una hora al itinerario",
    ),
    CommandData(
        callback=del_hour_cmd,
        name="del_hour",
        description="(admin) Quita una hora del itinerario",
    ),
    CommandData(
        callback=add_staff_cmd,
        name="add_staff",
        description="(dueño) Agrega un usuario al staff",
    ),
    CommandData(
        callback=initialize_cmd,
        name="init",
        description="Inicializa el bot",
    ),
    CommandData(
        callback=set_bd_cmd,
        name="set_bd",
        description="Configura tu cumpleaños",
    ),
    CommandData(
        callback=set_bd_manual_cmd,
        name="set_bd_manual",
        description="(admin) configura el cumpleaños de un usuario",
    ),
    CommandData(
        callback=set_offset_cmd,
        name="set_offset",
        description="(admin) Configura el offset",
    ),
    CommandData(
        callback=show_bd_cmd,
        name="show_bd",
        description="Muestra el listado de cumpleaños en este chat",
    ),
    CommandData(
        callback=show_hours_cmd,
        name="show_hours",
        description="Muestra el itinerario de horas",
    ),
    CommandData(
        callback=trigger_bd_message_check_cmd,
        name="trigger",
        description="none",
    ),
    CommandData(
        callback=set_congrats_message_cmd,
        name="set_congrats_message",
        description="Configura el mensaje de cumpleaños",
    ),
    CommandData(
        callback=show_cur_hour_cmd,
        name="show_cur_hour",
        description="Muestra la hora actual (con el offset aplicado)",
    ),
]
