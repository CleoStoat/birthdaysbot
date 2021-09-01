from datetime import datetime
from dataclasses import dataclass


@dataclass()
class Birthday:
    user_id: int
    day: int
    month: int


@dataclass()
class GroupConfig:
    chat_id: int
    offset: int
    congrats_message: str


@dataclass()
class GroupHour:
    chat_id: int
    hour: int


@dataclass()
class Staff:
    user_id: int
