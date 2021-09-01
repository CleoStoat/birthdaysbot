from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

import config
from domain.model import Birthday, GroupConfig, GroupHour, Staff
from sqlalchemy.orm import Session, session


class AbstractRepository(ABC):
    @abstractmethod
    def get_staff_list(self) -> List[Staff]:
        raise NotImplementedError

    @abstractmethod
    def add_staff_member(self, user_id):
        raise NotImplementedError

    @abstractmethod
    def rem_staff_member(self, user_id):
        raise NotImplementedError

    @abstractmethod
    def get_group_config(self, chat_id: int) -> Optional[GroupConfig]:
        raise NotImplementedError

    @abstractmethod
    def get_all_group_config(self) -> List[GroupConfig]:
        raise NotImplementedError

    @abstractmethod
    def add_group_config(self, chat_id: int, offset: int = None, congrats_message: str = None):
        raise NotImplementedError

    @abstractmethod
    def set_offset(self, chat_id: int, offset: int):
        raise NotImplementedError

    @abstractmethod
    def add_hour(self, chat_id: int, hour: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def del_hour(self, chat_id: int, hour: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_hours(self, chat_id: int) -> List[GroupHour]:
        raise NotImplementedError

    @abstractmethod
    def get_bd_list(self) -> List[Birthday]:
        raise NotImplementedError

    @abstractmethod
    def get_bd_list_at_date(self, curr_day: int, curr_month: int) -> List[Birthday]:
        raise NotImplementedError

    @abstractmethod
    def add_bd(self, user_id: int, day: int, month: int):
        raise NotImplementedError

    @abstractmethod
    def update_bd(self, user_id: int, day: int, month: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_bd(self, user_id: int) -> Optional[Birthday]:
        raise NotImplementedError

    @abstractmethod
    def set_congrats_message(self, chat_id: int, congrats_message: str):
        raise NotImplementedError

    @abstractmethod
    def get_congrats_message(self, chat_id: int) -> str:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def get_staff_list(self) -> List[Staff]:
        return self.session.query(Staff).all()

    def get_group_config(self, chat_id: int) -> Optional[GroupConfig]:
        return (
            self.session.query(GroupConfig)
            .filter(GroupConfig.chat_id == chat_id)
            .first()
        )

    def add_group_config(self, chat_id: int, offset: int = None, congrats_message: str = None):
        if offset is None:
            offset = config.get_default_offset()

        if congrats_message is None:
            congrats_message = config.get_default_congrats_message()

        group_config = GroupConfig(chat_id=chat_id, offset=offset, congrats_message=congrats_message)
        self.session.add(group_config)

    def set_offset(self, chat_id: int, offset: int):
        self.session.query(GroupConfig).filter(GroupConfig.chat_id == chat_id).update(
            {GroupConfig.offset: offset}
        )

    def add_hour(self, chat_id: int, hour: int) -> bool:
        group_hour = GroupHour(chat_id=chat_id, hour=hour)
        self.session.add(group_hour)

    def del_hour(self, chat_id: int, hour: int) -> bool:
        self.session.query(GroupHour).filter(GroupHour.chat_id == chat_id, GroupHour.hour == hour).delete()

    def get_hours(self, chat_id: int) -> List[GroupHour]:
        return self.session.query(GroupHour).filter(GroupHour.chat_id == chat_id).all()

    def get_bd_list(self) -> List[Birthday]:
        return self.session.query(Birthday).all()

    def get_bd_list_at_date(self, curr_day: int, curr_month: int) -> List[Birthday]:
        return self.session.query(Birthday).filter(
            Birthday.day == curr_day, Birthday.month == curr_month
        )

    def add_bd(self, user_id: int, day: int, month: int):
        birthday = Birthday(user_id=user_id, day=day, month=month)
        self.session.add(birthday)

    def update_bd(self, user_id: int, day: int, month: int) -> bool:
        self.session.query(Birthday).filter(Birthday.user_id == user_id).update(
            {Birthday.day: day, Birthday.month: month}
        )

    def get_bd(self, user_id: int) -> Optional[Birthday]:
        return self.session.query(Birthday).filter(Birthday.user_id == user_id).first()

    def add_staff_member(self, user_id):
        staff = Staff(user_id=user_id)
        self.session.add(staff)

    def rem_staff_member(self, user_id):
        self.session.query(Staff).filter(Staff.user_id == user_id).delete()

    def get_all_group_config(self) -> List[GroupConfig]:
        return self.session.query(GroupConfig).all()

    def set_congrats_message(self, chat_id: int, congrats_message: str):
        self.session.query(GroupConfig).filter(GroupConfig.chat_id == chat_id).update(
            {GroupConfig.congrats_message: congrats_message}
        )

    def get_congrats_message(self, chat_id: int) -> str:
        group_config = self.session.query(GroupConfig).filter(GroupConfig.chat_id == chat_id).first()

        if group_config is None:
            return ""
        else:
            return group_config.congrats_message