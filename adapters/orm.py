from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import mapper, relationship

from domain.model import Birthday, GroupConfig, GroupHour, Staff
import config

metadata = MetaData()

birthday = Table(
    "birthday",
    metadata,
    Column("user_id", Integer, primary_key=True, autoincrement=False),
    Column("day", Integer),
    Column("month", Integer),
)

group_config = Table(
    "group_config",
    metadata,
    Column("chat_id", Integer, primary_key=True, autoincrement=False),
    Column("offset", Integer),
    Column("congrats_message", String),
)

group_hour = Table(
    "group_hour",
    metadata,
    Column("chat_id", Integer, primary_key=True, autoincrement=False),
    Column("hour", Integer, primary_key=True, autoincrement=False),
)

staff = Table(
    "staff",
    metadata,
    Column("user_id", Integer, primary_key=True, autoincrement=False),
)

def start_mappers():
    mapper(Birthday, birthday)
    mapper(GroupConfig, group_config)
    mapper(GroupHour, group_hour)
    mapper(Staff, staff)


def create_tables():
    engine = create_engine(config.get_sqlite_uri())
    metadata.create_all(engine)
